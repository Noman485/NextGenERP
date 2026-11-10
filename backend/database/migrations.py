"""Small, dependency-free schema migrations for existing NextGenERP databases.

The project intentionally avoids a full migration framework.  ``create_all``
creates missing tables but never adds columns to an existing table, so this
module applies the additive changes needed by the administrator features.  It
is safe to run repeatedly and works on both SQLite and PostgreSQL.
"""

from __future__ import annotations

import logging

from sqlalchemy import inspect, text

from database.connection import engine

logger = logging.getLogger(__name__)


def _dialect() -> str:
    return engine.dialect.name


def _table_columns(table: str) -> set[str]:
    inspector = inspect(engine)
    if table not in inspector.get_table_names():
        return set()
    return {column["name"] for column in inspector.get_columns(table)}


def _index_names(table: str) -> set[str]:
    inspector = inspect(engine)
    if table not in inspector.get_table_names():
        return set()
    return {index["name"] for index in inspector.get_indexes(table)}


def _add_column(table: str, column: str, definition: str) -> None:
    if column in _table_columns(table):
        return
    with engine.begin() as connection:
        connection.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {definition}"))
    logger.info("Added column %s.%s", table, column)


def _add_index(table: str, name: str, columns: str, unique: bool = False) -> None:
    if name in _index_names(table):
        return
    unique_sql = "UNIQUE " if unique else ""
    with engine.begin() as connection:
        connection.execute(
            text(f"CREATE {unique_sql}INDEX IF NOT EXISTS {name} ON {table} ({columns})")
        )
    logger.info("Added index %s on %s", name, table)


def ensure_schema() -> None:
    """Apply additive schema changes required by the current application."""

    dialect = _dialect()
    timestamp_type = "TIMESTAMP WITH TIME ZONE" if dialect == "postgresql" else "DATETIME"
    boolean_true = "TRUE" if dialect == "postgresql" else "1"
    boolean_false = "FALSE" if dialect == "postgresql" else "0"

    _add_column("users", "email", "VARCHAR(255)")
    _add_column("users", "role", "VARCHAR(20) NOT NULL DEFAULT 'USER'")
    _add_column(
        "users",
        "is_active",
        f"BOOLEAN NOT NULL DEFAULT {boolean_true}",
    )
    _add_column("users", "last_login_at", timestamp_type)

    _add_column("orders", "user_id", "INTEGER REFERENCES users(id)")
    _add_column("orders", "created_at", timestamp_type)
    _add_column("purchase_orders", "created_at", timestamp_type)

    _add_index("users", "ix_users_email", "email", unique=True)
    _add_index("users", "ix_users_role", "role")
    _add_index("orders", "ix_orders_user_id", "user_id")
    _add_index("orders", "ix_orders_created_at", "created_at")
    _add_index("purchase_orders", "ix_purchase_orders_created_at", "created_at")

    with engine.begin() as connection:
        connection.execute(
            text("UPDATE users SET role = 'USER' WHERE role IS NULL OR role = ''")
        )
        connection.execute(
            text(
                "UPDATE users SET is_active = "
                f"{boolean_true} WHERE is_active IS NULL"
            )
        )
        # Older SQLite databases may have stored the boolean as text.
        if dialect != "postgresql":
            connection.execute(
                text(
                    "UPDATE users SET is_active = "
                    f"{boolean_false} WHERE is_active = '0'"
                )
            )

    logger.info("Schema check complete")
