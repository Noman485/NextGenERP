from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from admin_provision import normalize_email
from auth.dependencies import get_current_user
from auth.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    DUMMY_PASSWORD_HASH,
    create_access_token,
    hash_password,
    verify_password,
)
from auth.tokens import (
    hash_refresh_token,
    is_expired,
    issue_refresh_token,
    revoke_family,
    revoke_family_for_token,
    utcnow,
)
from database.connection import engine
from models.refresh_token import RefreshToken
from models.user import User
from schemas.auth import (
    RefreshTokenRequest,
    TokenResponse,
    UserLogin,
    UserRegistration,
    UserResponse,
)
from security_controls import check_rate_limit, client_ip
from services.audit import commit_audit, record_audit, user_state

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_db():
    with Session(engine) as session:
        yield session


def _issue_session_tokens(
    db: Session,
    user: User,
    request: Request,
    family_id: str | None = None,
):
    """Create a refresh-token session and its bound access token."""

    raw_refresh, refresh_entry = issue_refresh_token(
        db, user, family_id=family_id, request=request
    )
    access_token = create_access_token(
        user.id, session_id=refresh_entry.family_id
    )
    return access_token, raw_refresh, refresh_entry


def _token_response(
    access_token: str,
    refresh_token: str,
    user: User,
) -> TokenResponse:
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.model_validate(user),
    )


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserRegistration,
    request: Request,
    db: Session = Depends(get_db),
):
    check_rate_limit(request, "register_ip")
    check_rate_limit(
        request,
        "register",
        identity=f"{client_ip(request)}:{user_data.username.strip().lower()}",
    )
    username = user_data.username.strip().lower()
    try:
        email = normalize_email(user_data.email)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    if db.query(User).filter(User.username == username).first() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username is already registered",
        )
    if email and db.query(User).filter(User.email == email).first() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        )

    user = User(
        username=username,
        email=email,
        password_hash=hash_password(user_data.password),
        role="USER",
        is_active=True,
    )
    try:
        db.add(user)
        db.flush()
        access_token, refresh_token, _ = _issue_session_tokens(db, user, request)
        record_audit(
            db,
            action="auth.register",
            entity_type="user",
            entity_id=user.id,
            actor=user,
            after=user_state(user),
            request=request,
        )
        db.commit()
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email is already registered",
        ) from error
    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to register account",
        ) from error

    db.refresh(user)
    return _token_response(access_token, refresh_token, user)


@router.post("/login", response_model=TokenResponse)
def login(
    user_data: UserLogin,
    request: Request,
    db: Session = Depends(get_db),
):
    check_rate_limit(request, "login_ip")
    check_rate_limit(
        request,
        "login",
        identity=f"{client_ip(request)}:{user_data.username.strip().lower()}",
    )
    user = (
        db.query(User)
        .filter(User.username == user_data.username.strip().lower())
        .first()
    )
    hashed_password = user.password_hash if user is not None else DUMMY_PASSWORD_HASH
    if not verify_password(user_data.password, hashed_password) or user is None:
        record_audit(
            db,
            action="auth.login_failed",
            entity_type="user",
            entity_id=user.id if user is not None else None,
            actor_user_id=user.id if user is not None else None,
            actor_username=user_data.username.strip().lower(),
            outcome="failure",
            request=request,
        )
        commit_audit(db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        record_audit(
            db,
            action="auth.login_denied",
            entity_type="user",
            entity_id=user.id,
            actor=user,
            outcome="denied",
            request=request,
        )
        commit_audit(db)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account has been deactivated",
        )

    before = user_state(user)
    user.last_login_at = datetime.now(timezone.utc)
    record_audit(
        db,
        action="auth.login",
        entity_type="user",
        entity_id=user.id,
        actor=user,
        before=before,
        after=user_state(user),
        request=request,
    )
    access_token, refresh_token, _ = _issue_session_tokens(db, user, request)
    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()

    return _token_response(access_token, refresh_token, user)


@router.get("/me", response_model=UserResponse)
def get_me(user: User = Depends(get_current_user)):
    return user


@router.post("/refresh", response_model=TokenResponse)
def refresh_session(
    payload: RefreshTokenRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    entry = (
        db.query(RefreshToken)
        .filter(RefreshToken.token_hash == hash_refresh_token(payload.refresh_token))
        .first()
    )
    if entry is None:
        record_audit(
            db,
            action="auth.refresh_failed",
            entity_type="session",
            outcome="failure",
            request=request,
        )
        commit_audit(db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.get(User, entry.user_id)

    if entry.revoked_at is not None:
        reused = entry.replaced_by_id is not None
        if reused:
            # A rotated token was presented again. Assume theft and invalidate
            # the entire session family, including the current child token.
            revoke_family(db, entry.family_id)
        record_audit(
            db,
            action=(
                "auth.refresh_reuse_detected"
                if reused
                else "auth.refresh_denied"
            ),
            entity_type="session",
            entity_id=entry.id,
            actor_user_id=entry.user_id,
            actor_username=user.username if user is not None else None,
            outcome="denied",
            request=request,
        )
        commit_audit(db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if is_expired(entry.expires_at) or user is None:
        record_audit(
            db,
            action="auth.refresh_failed",
            entity_type="session",
            entity_id=entry.id,
            actor_user_id=entry.user_id,
            actor_username=user.username if user is not None else None,
            outcome="failure",
            request=request,
        )
        commit_audit(db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        revoke_family(db, entry.family_id)
        record_audit(
            db,
            action="auth.refresh_denied",
            entity_type="session",
            entity_id=entry.id,
            actor_user_id=entry.user_id,
            actor_username=user.username,
            outcome="denied",
            request=request,
        )
        commit_audit(db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    entry.revoked_at = utcnow()
    entry.last_used_at = entry.revoked_at
    access_token, refresh_token, new_entry = _issue_session_tokens(
        db, user, request, family_id=entry.family_id
    )
    entry.replaced_by_id = new_entry.id
    record_audit(
        db,
        action="auth.refresh",
        entity_type="session",
        entity_id=new_entry.id,
        actor=user,
        after={"rotated": True},
        request=request,
    )
    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to refresh session",
        )
    db.refresh(user)
    return _token_response(access_token, refresh_token, user)


@router.post("/logout")
def logout(
    payload: RefreshTokenRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """Revoke the refresh-token family for this session.

    The endpoint is intentionally idempotent and does not reveal whether a
    token existed. Access tokens carry the family id, so a successful logout
    invalidates them immediately on the next request.
    """

    entry = revoke_family_for_token(db, payload.refresh_token)
    if entry is not None:
        user = db.get(User, entry.user_id)
        record_audit(
            db,
            action="auth.logout",
            entity_type="session",
            entity_id=entry.id,
            actor=user,
            actor_user_id=entry.user_id,
            request=request,
        )
        try:
            db.commit()
        except SQLAlchemyError:
            db.rollback()
    return {"detail": "Signed out"}
