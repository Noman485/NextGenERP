"""Refresh-token session management.

Refresh tokens are opaque random values. Only their SHA-256 hash is stored, so
a database leak does not expose usable credentials. Every rotation shares a
``family_id``; presenting a rotated token again is treated as reuse and revokes
the whole family. Access tokens carry the family id in their ``sid`` claim so a
logout can invalidate them immediately instead of waiting for expiry.
"""

from __future__ import annotations

import hashlib
import os
import secrets
import uuid
from datetime import datetime, timedelta, timezone

from fastapi import Request
from sqlalchemy.orm import Session

from database.connection import engine
from models.refresh_token import RefreshToken

DEFAULT_REFRESH_TOKEN_EXPIRE_DAYS = 7


def refresh_token_expire_days() -> int:
    raw = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "").strip()
    if raw.isdigit():
        value = int(raw)
        if 1 <= value <= 30:
            return value
    return DEFAULT_REFRESH_TOKEN_EXPIRE_DAYS


def hash_refresh_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def normalize_utc(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def is_expired(value: datetime | None, now: datetime | None = None) -> bool:
    normalized = normalize_utc(value)
    if normalized is None:
        return True
    return normalized <= (now or utcnow())


def issue_refresh_token(
    db: Session,
    user,
    *,
    family_id: str | None = None,
    request: Request | None = None,
) -> tuple[str, RefreshToken]:
    """Create and flush a new refresh-token row; return (raw token, row)."""

    raw_token = secrets.token_urlsafe(48)
    now = utcnow()
    user_agent = None
    ip_address = None
    if request is not None:
        user_agent = request.headers.get("user-agent")
        ip_address = request.client.host if request.client else None

    entry = RefreshToken(
        user_id=user.id,
        token_hash=hash_refresh_token(raw_token),
        family_id=family_id or uuid.uuid4().hex,
        issued_at=now,
        expires_at=now + timedelta(days=refresh_token_expire_days()),
        user_agent=(user_agent or "")[:255] or None,
        ip_address=ip_address,
    )
    db.add(entry)
    db.flush()
    return raw_token, entry


def revoke_family(db: Session, family_id: str) -> None:
    """Revoke every refresh token in a session family."""

    db.query(RefreshToken).filter(
        RefreshToken.family_id == family_id,
        RefreshToken.revoked_at.is_(None),
    ).update(
        {RefreshToken.revoked_at: utcnow()},
        synchronize_session=False,
    )


def session_is_active(family_id: str, user_id: int) -> bool:
    """Return True when the family still has a live, unrevoked token."""

    with Session(engine) as session:
        rows = (
            session.query(RefreshToken)
            .filter(
                RefreshToken.family_id == family_id,
                RefreshToken.user_id == user_id,
                RefreshToken.revoked_at.is_(None),
            )
            .all()
        )
        now = utcnow()
        return any(not is_expired(row.expires_at, now) for row in rows)


def revoke_family_for_token(db: Session, raw_token: str, user_id: int | None = None) -> RefreshToken | None:
    """Revoke the family owning ``raw_token``; return the matched row."""

    query = db.query(RefreshToken).filter(
        RefreshToken.token_hash == hash_refresh_token(raw_token)
    )
    if user_id is not None:
        query = query.filter(RefreshToken.user_id == user_id)
    entry = query.first()
    if entry is not None:
        revoke_family(db, entry.family_id)
        entry.revoked_at = entry.revoked_at or utcnow()
    return entry
