"""Alembic environment for NextGenERP.

The application reads ``DATABASE_URL`` through ``database.connection``; this
environment reuses that engine so CLI migrations and the running app always
target the same database. The URL in ``alembic.ini`` is intentionally unused.
"""

from __future__ import annotations

from logging.config import fileConfig

from alembic import context

from database.connection import Base, engine

# Import every model module so ``Base.metadata`` is complete for autogenerate.
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

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def _database_url() -> str:
    return engine.url.render_as_string(hide_password=False)


def run_migrations_offline() -> None:
    context.configure(
        url=_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            render_as_batch=engine.dialect.name == "sqlite",
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
