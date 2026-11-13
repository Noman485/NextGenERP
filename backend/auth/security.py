import os
import re
import secrets
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()
DUMMY_PASSWORD_HASH = password_hash.hash(secrets.token_urlsafe(32))
ACCESS_TOKEN_EXPIRE_MINUTES = 30
JWT_ALGORITHM = "HS256"
_SESSION_ID_PATTERN = re.compile(r"^[A-Za-z0-9-]{8,64}$")


@dataclass(frozen=True)
class AccessTokenClaims:
    user_id: int
    session_id: str | None = None


def _jwt_secret() -> str:
    secret = os.getenv("JWT_SECRET_KEY", "")
    if len(secret) < 32:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication is not configured on this server",
        )
    return secret


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_access_token(user_id: int, session_id: str | None = None) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "jti": uuid.uuid4().hex,
    }
    if session_id is not None:
        if not _SESSION_ID_PATTERN.fullmatch(session_id):
            raise ValueError("Invalid session id")
        payload["sid"] = session_id
    return jwt.encode(payload, _jwt_secret(), algorithm=JWT_ALGORITHM)


def decode_access_token_claims(token: str) -> AccessTokenClaims:
    try:
        payload = jwt.decode(
            token,
            _jwt_secret(),
            algorithms=[JWT_ALGORITHM],
            options={"require": ["sub", "exp"]},
        )
        subject = payload.get("sub")
        if (
            not isinstance(subject, str)
            or not subject.isascii()
            or not subject.isdigit()
        ):
            raise jwt.InvalidTokenError("Invalid token subject")
        user_id = int(subject)
        # Keep database lookups inside the signed 64-bit integer range used by
        # both SQLite and PostgreSQL. A syntactically valid but absurd subject
        # must be rejected as a bad token, not allowed to reach the driver.
        if user_id < 1 or user_id > 2**63 - 1:
            raise jwt.InvalidTokenError("Invalid token subject")

        session_id = payload.get("sid")
        if session_id is not None and (
            not isinstance(session_id, str)
            or not _SESSION_ID_PATTERN.fullmatch(session_id)
        ):
            raise jwt.InvalidTokenError("Invalid token session")
        return AccessTokenClaims(user_id=user_id, session_id=session_id)
    except HTTPException:
        raise
    except jwt.InvalidTokenError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from error


def decode_access_token(token: str) -> int:
    """Return the user id from a token (kept for existing callers)."""

    return decode_access_token_claims(token).user_id
