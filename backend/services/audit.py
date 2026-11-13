"""Append-only audit trail and request-correlation helpers.

Audit rows are written inside the caller's transaction so a successful
business change and its audit record commit together. Failed operations that
still matter for security (for example a failed login) use
``commit_audit`` explicitly.
"""

from __future__ import annotations

import logging
from contextvars import ContextVar
from datetime import date, datetime
from typing import Any

from fastapi import Request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models.audit_log import AuditLog

logger = logging.getLogger(__name__)

_request_id: ContextVar[str | None] = ContextVar("request_id", default=None)
MAX_STRING_LENGTH = 500
MAX_DEPTH = 4

SENSITIVE_MARKERS = (
    "password",
    "passwd",
    "secret",
    "token",
    "authorization",
    "api_key",
    "apikey",
    "hash",
    "cookie",
    "private_key",
)


def set_request_id(value: str | None):
    """Bind a request id to the current async context."""

    return _request_id.set(value)


def reset_request_id(token) -> None:
    _request_id.reset(token)


def current_request_id() -> str | None:
    return _request_id.get()


def _is_sensitive_key(key: str) -> bool:
    lowered = key.lower()
    return any(marker in lowered for marker in SENSITIVE_MARKERS)


def sanitize(value: Any, depth: int = 0) -> Any:
    """Return a JSON-safe copy with secrets removed and strings bounded."""

    if depth > MAX_DEPTH:
        return "[truncated]"
    if value is None or isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, str):
        return value[:MAX_STRING_LENGTH]
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, dict):
        return {
            str(key): "[redacted]" if _is_sensitive_key(str(key)) else sanitize(item, depth + 1)
            for key, item in value.items()
        }
    if isinstance(value, (list, tuple, set)):
        return [sanitize(item, depth + 1) for item in value]
    return str(value)[:MAX_STRING_LENGTH]


def model_state(instance: Any, fields: tuple[str, ...]) -> dict[str, Any]:
    """Take a sanitized snapshot of selected model attributes."""

    return {
        field: sanitize(getattr(instance, field, None))
        for field in fields
    }


PRODUCT_FIELDS = (
    "id",
    "name",
    "sku",
    "price",
    "stock_quantity",
    "reorder_level",
    "category_id",
)
CATEGORY_FIELDS = ("id", "name", "description")
SUPPLIER_FIELDS = (
    "id",
    "name",
    "email",
    "phone",
    "address",
    "lead_time_days",
    "performance_rating",
)
ORDER_FIELDS = (
    "id",
    "customer_name",
    "customer_email",
    "product_id",
    "quantity",
    "total_amount",
    "status",
    "user_id",
    "created_at",
)
PURCHASE_ORDER_FIELDS = (
    "id",
    "supplier_id",
    "product_id",
    "quantity",
    "unit_price",
    "total_amount",
    "status",
    "created_at",
)
INVENTORY_FIELDS = (
    "id",
    "product_id",
    "transaction_type",
    "quantity",
    "previous_stock",
    "new_stock",
    "reason",
    "created_at",
)
USER_FIELDS = ("id", "username", "email", "role", "is_active", "created_at", "last_login_at")


def product_state(product) -> dict[str, Any]:
    return model_state(product, PRODUCT_FIELDS)


def category_state(category) -> dict[str, Any]:
    return model_state(category, CATEGORY_FIELDS)


def supplier_state(supplier) -> dict[str, Any]:
    return model_state(supplier, SUPPLIER_FIELDS)


def order_state(order) -> dict[str, Any]:
    return model_state(order, ORDER_FIELDS)


def purchase_order_state(purchase_order) -> dict[str, Any]:
    return model_state(purchase_order, PURCHASE_ORDER_FIELDS)


def inventory_state(transaction) -> dict[str, Any]:
    return model_state(transaction, INVENTORY_FIELDS)


def user_state(user) -> dict[str, Any]:
    return model_state(user, USER_FIELDS)


def record_audit(
    db: Session,
    *,
    action: str,
    entity_type: str,
    entity_id: int | None = None,
    actor=None,
    actor_user_id: int | None = None,
    actor_username: str | None = None,
    before: dict | None = None,
    after: dict | None = None,
    outcome: str = "success",
    request: Request | None = None,
) -> AuditLog:
    """Add an audit entry to the current transaction.

    The caller is responsible for committing. ``actor`` may be a User model;
    secrets are never copied because snapshots only include explicit fields and
    every value passes through ``sanitize``.
    """

    request_id = current_request_id()
    ip_address = None
    if request is not None:
        request_id = getattr(request.state, "request_id", request_id)
        ip_address = request.client.host if request.client else None

    if actor is not None:
        actor_user_id = getattr(actor, "id", actor_user_id)
        actor_username = getattr(actor, "username", actor_username)

    entry = AuditLog(
        actor_user_id=actor_user_id,
        actor_username=sanitize(actor_username),
        action=action[:80],
        entity_type=entity_type[:40],
        entity_id=entity_id,
        outcome=outcome[:20],
        request_id=sanitize(request_id),
        ip_address=sanitize(ip_address),
        before_values=sanitize(before) if before is not None else None,
        after_values=sanitize(after) if after is not None else None,
    )
    db.add(entry)
    return entry


def commit_audit(db: Session) -> bool:
    """Commit an audit-only transaction, never raising into the request path."""

    try:
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        logger.warning("Unable to persist audit event", exc_info=False)
        return False
