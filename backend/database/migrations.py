"""Small, dependency-free schema migrations for existing NextGenERP databases.

The project intentionally avoids a full migration framework.  ``create_all``
creates missing tables but never adds columns to an existing table, so this
module applies the additive changes needed by the administrator features.  It
is safe to run repeatedly and works on both SQLite and PostgreSQL.
"""

from __future__ import annotations

import logging

from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError

from database.connection import engine

logger = logging.getLogger(__name__)

# Checks mirror the validation in the API schemas and the model-level
# ``CheckConstraint`` declarations. They are installed as triggers on existing
# SQLite databases because SQLite cannot add a CHECK to a populated table
# without rebuilding it.
SQLITE_INTEGRITY_TRIGGERS = {
    "products": (
        "NEW.price < 0 OR NEW.stock_quantity < 0 OR NEW.reorder_level < 0",
        "UPDATE OF price, stock_quantity, reorder_level ON products",
    ),
    "orders": (
        "NEW.quantity <= 0 OR NEW.total_amount < 0 OR NEW.status NOT IN "
        "('Pending', 'Confirmed', 'Shipped', 'Delivered', 'Cancelled')",
        "UPDATE OF quantity, total_amount, status ON orders",
    ),
    "purchase_orders": (
        "NEW.quantity <= 0 OR NEW.unit_price < 0 OR NEW.total_amount < 0 "
        "OR NEW.status NOT IN "
        "('Pending', 'Approved', 'Ordered', 'Received', 'Cancelled')",
        "UPDATE OF quantity, unit_price, total_amount, status ON purchase_orders",
    ),
    "suppliers": (
        "NEW.lead_time_days < 0 OR NEW.performance_rating < 0 "
        "OR NEW.performance_rating > 5",
        "UPDATE OF lead_time_days, performance_rating ON suppliers",
    ),
}

POSTGRES_INTEGRITY_CONSTRAINTS = {
    "products": {
        "ck_products_price_non_negative": "price >= 0",
        "ck_products_stock_non_negative": "stock_quantity >= 0",
        "ck_products_reorder_non_negative": "reorder_level >= 0",
    },
    "orders": {
        "ck_orders_quantity_positive": "quantity > 0",
        "ck_orders_total_non_negative": "total_amount >= 0",
        "ck_orders_status_valid": (
            "status IN ('Pending', 'Confirmed', 'Shipped', 'Delivered', 'Cancelled')"
        ),
    },
    "purchase_orders": {
        "ck_purchase_orders_quantity_positive": "quantity > 0",
        "ck_purchase_orders_unit_price_non_negative": "unit_price >= 0",
        "ck_purchase_orders_total_non_negative": "total_amount >= 0",
        "ck_purchase_orders_status_valid": (
            "status IN ('Pending', 'Approved', 'Ordered', 'Received', 'Cancelled')"
        ),
    },
    "suppliers": {
        "ck_suppliers_lead_time_non_negative": "lead_time_days >= 0",
        "ck_suppliers_rating_range": (
            "performance_rating IS NULL OR "
            "(performance_rating >= 0 AND performance_rating <= 5)"
        ),
    },
}


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


def _ensure_audit_append_only() -> None:
    """Install database-level guards that keep the audit trail append-only."""

    if "audit_logs" not in inspect(engine).get_table_names():
        return

    if _dialect() == "postgresql":
        with engine.begin() as connection:
            connection.execute(
                text(
                    """
                    CREATE OR REPLACE FUNCTION nextgenerp_audit_append_only()
                    RETURNS trigger AS $$
                    BEGIN
                        RAISE EXCEPTION 'audit_logs is append-only';
                    END;
                    $$ LANGUAGE plpgsql
                    """
                )
            )
            connection.execute(
                text("DROP TRIGGER IF EXISTS audit_logs_append_only ON audit_logs")
            )
            connection.execute(
                text(
                    """
                    CREATE TRIGGER audit_logs_append_only
                    BEFORE UPDATE OR DELETE ON audit_logs
                    FOR EACH ROW EXECUTE FUNCTION nextgenerp_audit_append_only()
                    """
                )
            )
        return

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                CREATE TRIGGER IF NOT EXISTS audit_logs_no_update
                BEFORE UPDATE ON audit_logs
                BEGIN
                    SELECT RAISE(ABORT, 'audit_logs is append-only');
                END
                """
            )
        )
        connection.execute(
            text(
                """
                CREATE TRIGGER IF NOT EXISTS audit_logs_no_delete
                BEFORE DELETE ON audit_logs
                BEGIN
                    SELECT RAISE(ABORT, 'audit_logs is append-only');
                END
                """
            )
        )


def _constraint_names(table: str) -> set[str]:
    inspector = inspect(engine)
    if table not in inspector.get_table_names():
        return set()
    return {
        constraint["name"]
        for constraint in inspector.get_check_constraints(table)
        if constraint.get("name")
    }


def _ensure_data_integrity() -> None:
    """Enforce non-negative amounts and valid statuses at the database level.

    Fresh databases already receive CHECK constraints from the SQLAlchemy
    models. Existing SQLite databases cannot gain a CHECK constraint without a
    table rebuild, so equivalent BEFORE INSERT/UPDATE triggers are installed.
    PostgreSQL gets the constraints as ``NOT VALID`` first: new and updated
    rows are checked immediately while legacy rows are left untouched, which
    keeps startup safe for databases created before these rules existed.
    """

    tables = set(inspect(engine).get_table_names())

    if _dialect() == "postgresql":
        for table, constraints in POSTGRES_INTEGRITY_CONSTRAINTS.items():
            if table not in tables:
                continue
            existing = _constraint_names(table)
            for name, expression in constraints.items():
                if name in existing:
                    continue
                try:
                    with engine.begin() as connection:
                        connection.execute(
                            text(
                                f"ALTER TABLE {table} ADD CONSTRAINT {name} "
                                f"CHECK ({expression}) NOT VALID"
                            )
                        )
                    logger.info("Added integrity constraint %s", name)
                except SQLAlchemyError:
                    logger.warning(
                        "Could not add integrity constraint %s on %s",
                        name,
                        table,
                        exc_info=False,
                    )
        return

    for table, (condition, update_statement) in SQLITE_INTEGRITY_TRIGGERS.items():
        if table not in tables:
            continue
        with engine.begin() as connection:
            connection.execute(
                text(
                    f"""
                    CREATE TRIGGER IF NOT EXISTS {table}_integrity_insert
                    BEFORE INSERT ON {table}
                    FOR EACH ROW WHEN {condition}
                    BEGIN
                        SELECT RAISE(ABORT, '{table} integrity constraint violated');
                    END
                    """
                )
            )
            connection.execute(
                text(
                    f"""
                    CREATE TRIGGER IF NOT EXISTS {table}_integrity_update
                    BEFORE {update_statement}
                    FOR EACH ROW WHEN {condition}
                    BEGIN
                        SELECT RAISE(ABORT, '{table} integrity constraint violated');
                    END
                    """
                )
            )


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

    _ensure_audit_append_only()
    _ensure_data_integrity()

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
