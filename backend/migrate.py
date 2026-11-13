"""Bootstrap or upgrade the database schema with Alembic.

Usage (from ``backend``):

    python migrate.py

Fresh databases are created by the baseline Alembic revision. Databases that
predate Alembic are brought to the current schema with the existing additive
``create_all``/``ensure_schema`` helpers and then stamped at head, so their data
is preserved and future changes are versioned. PostgreSQL is verified only when
a real service is available; see ``docs/MIGRATIONS.md``.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import inspect

from database.connection import Base, engine
from database.migrations import ensure_schema

# Import all models so Base.metadata is complete before create_all.
from models import (  # noqa: F401
    audit_log,
    category,
    inventory_transaction,
    order,
    product,
    purchase_order,
    refresh_token,
    supplier,
    user,
)

logger = logging.getLogger("nextgenerp.migrate")

APP_TABLES = {
    "users",
    "categories",
    "products",
    "suppliers",
    "orders",
    "purchase_orders",
    "inventory_transactions",
    "audit_logs",
    "refresh_tokens",
}


def alembic_config() -> Config:
    return Config(str(Path(__file__).with_name("alembic.ini")))


def schema_state() -> tuple[bool, bool]:
    """Return (has_app_tables, has_alembic_version)."""

    inspector = inspect(engine)
    tables = set(inspector.get_table_names())
    return bool(tables & APP_TABLES), "alembic_version" in tables


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    config = alembic_config()
    has_app_tables, is_versioned = schema_state()

    if not is_versioned and has_app_tables:
        logger.info(
            "Existing unversioned database detected; applying additive schema "
            "updates and stamping the baseline"
        )
        Base.metadata.create_all(bind=engine)
        ensure_schema()
        command.stamp(config, "head")
        logger.info("Database stamped at Alembic head; data was not modified")
        return 0

    if not is_versioned:
        logger.info("Empty database detected; running Alembic migrations")
        command.upgrade(config, "head")
        logger.info("Database created at Alembic head")
        return 0

    command.upgrade(config, "head")
    logger.info("Database upgraded to Alembic head")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception:
        logging.getLogger("nextgenerp.migrate").exception("Database migration failed")
        sys.exit(1)
