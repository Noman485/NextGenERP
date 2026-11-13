from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from auth.security import decode_access_token_claims
from auth.tokens import session_is_active
from database.connection import engine
from models.user import User

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    claims = decode_access_token_claims(credentials.credentials)
    with Session(engine) as session:
        user = session.get(User, claims.user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This account has been deactivated",
            )
        session.expunge(user)

    # New tokens are bound to a server-side session family. Tokens minted
    # before the refresh-token upgrade have no ``sid`` claim and remain valid
    # until their normal 30-minute expiry (documented compatibility window).
    if claims.session_id is not None and not session_is_active(
        claims.session_id, user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def require_authenticated_user(user: User = Depends(get_current_user)) -> User:
    """Return the active signed-in user, or raise 401/403."""

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account has been deactivated",
        )
    return user


def require_role(*roles: str):
    """Build a dependency that requires one of the supplied roles."""

    allowed = {role.upper() for role in roles}

    def dependency(user: User = Depends(require_authenticated_user)) -> User:
        if (user.role or "USER").upper() not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )
        return user

    return dependency


require_admin = require_role("ADMIN")
