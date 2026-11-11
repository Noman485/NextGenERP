from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from admin_provision import normalize_email
from auth.dependencies import get_current_user
from auth.security import (
    DUMMY_PASSWORD_HASH,
    create_access_token,
    hash_password,
    verify_password,
)
from database.connection import engine
from models.user import User
from schemas.auth import TokenResponse, UserLogin, UserRegistration, UserResponse
from security_controls import check_rate_limit, client_ip

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_db():
    with Session(engine) as session:
        yield session


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
        access_token = create_access_token(user.id)
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
    return TokenResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user),
    )


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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account has been deactivated",
        )

    user.last_login_at = datetime.now(timezone.utc)
    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()

    return TokenResponse(
        access_token=create_access_token(user.id),
        user=UserResponse.model_validate(user),
    )


@router.get("/me", response_model=UserResponse)
def get_me(user: User = Depends(get_current_user)):
    return user
