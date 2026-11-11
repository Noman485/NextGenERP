"""Secure administrator provisioning helpers.

Administrators are never hardcoded and are never promoted by the public
registration endpoint.  Use the ``create_admin.py`` CLI, or set the optional
bootstrap environment variables before starting the backend.
"""

from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth.security import hash_password
from database.connection import engine
from models.user import User
from validation import normalize_email

logger = logging.getLogger(__name__)

USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_.-]{3,80}$")
MIN_PASSWORD_LENGTH = 12
MAX_PASSWORD_LENGTH = 128


@dataclass
class ProvisionResult:
    user: User
    created: bool


def validate_credentials(username: str, password: str) -> str:
    cleaned_username = username.strip().lower()
    if not USERNAME_PATTERN.match(cleaned_username):
        raise ValueError(
            "Username must be 3-80 characters using letters, numbers, dot, dash or underscore"
        )
    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValueError(f"Password must be at least {MIN_PASSWORD_LENGTH} characters")
    if len(password) > MAX_PASSWORD_LENGTH:
        raise ValueError(f"Password must be at most {MAX_PASSWORD_LENGTH} characters")
    return cleaned_username


def provision_admin(
    db: Session,
    username: str,
    password: str,
    email: str | None = None,
    *,
    promote: bool = False,
    reset_password: bool = False,
) -> ProvisionResult:
    """Create an administrator, or explicitly promote/reset an existing user.

    Existing accounts are never promoted implicitly.  ``promote`` must be set
    by an operator who already has database access.  ``reset_password`` is
    required to change an existing administrator's password.
    """

    cleaned_username = validate_credentials(username, password)
    cleaned_email = normalize_email(email)

    user = db.query(User).filter(User.username == cleaned_username).first()
    if user is None:
        user = User(
            username=cleaned_username,
            email=cleaned_email,
            password_hash=hash_password(password),
            role="ADMIN",
            is_active=True,
        )
        db.add(user)
        created = True
    else:
        if user.role != "ADMIN" and not promote:
            raise ValueError(
                "A normal user already has this username. Re-run with --promote "
                "only if this account should become an administrator."
            )
        if user.role == "ADMIN" and not reset_password and not promote:
            raise ValueError(
                "This administrator already exists. Use --reset-password to set a new password."
            )
        if not promote and not reset_password:
            raise ValueError("No change requested")
        user.role = "ADMIN"
        user.is_active = True
        user.password_hash = hash_password(password)
        if cleaned_email:
            user.email = cleaned_email
        created = False

    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()
        raise ValueError("Username or email is already registered") from error

    db.refresh(user)
    return ProvisionResult(user=user, created=created)


def bootstrap_admin_from_env() -> None:
    """Optionally create the first administrator from environment variables.

    Set ``ADMIN_BOOTSTRAP_USERNAME`` and ``ADMIN_BOOTSTRAP_PASSWORD`` once.
    The bootstrap is skipped when any administrator already exists.  Passwords
    are never written to logs.
    """

    username = os.getenv("ADMIN_BOOTSTRAP_USERNAME", "").strip()
    password = os.getenv("ADMIN_BOOTSTRAP_PASSWORD", "")
    if not username or not password:
        return

    with Session(engine) as db:
        existing_admin = db.query(User).filter(User.role == "ADMIN").first()
        if existing_admin is not None:
            return
        try:
            result = provision_admin(
                db,
                username,
                password,
                os.getenv("ADMIN_BOOTSTRAP_EMAIL"),
            )
        except ValueError as error:
            logger.error("Administrator bootstrap failed: %s", error)
            return
        logger.info("Bootstrapped administrator account %s", result.user.username)
