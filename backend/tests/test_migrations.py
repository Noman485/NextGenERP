"""Alembic migration tests on real temporary SQLite databases.

PostgreSQL migration verification requires a running service and is marked
BLOCKED in the security report; the same revisions are dialect-agnostic and are
exercised by CI when a PostgreSQL service is available.
"""

from __future__ import annotations

import os
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest
from sqlalchemy import create_engine, inspect

BACKEND_DIR = Path(__file__).resolve().parents[1]
LOCAL_DATABASE = BACKEND_DIR / "nextgenerp.db"


def run(
    args: list[str],
    database: Path,
    *,
    timeout: int = 120,
) -> subprocess.CompletedProcess:
    environment = os.environ.copy()
    environment["DATABASE_URL"] = f"sqlite:///{database.as_posix()}"
    return subprocess.run(
        [sys.executable, *args],
        cwd=BACKEND_DIR,
        env=environment,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def table_names(database: Path) -> set[str]:
    engine = create_engine(f"sqlite:///{database.as_posix()}")
    try:
        return set(inspect(engine).get_table_names())
    finally:
        engine.dispose()


def scalar(database: Path, query: str) -> object:
    connection = sqlite3.connect(database)
    try:
        return connection.execute(query).fetchone()[0]
    finally:
        connection.close()


def test_fresh_database_upgrades_and_downgrades(tmp_path):
    database = tmp_path / "fresh.db"

    upgraded = run(["-m", "alembic", "upgrade", "head"], database)
    assert upgraded.returncode == 0, upgraded.stderr
    assert {
        "users",
        "categories",
        "products",
        "suppliers",
        "orders",
        "purchase_orders",
        "inventory_transactions",
        "audit_logs",
        "refresh_tokens",
        "alembic_version",
    } <= table_names(database)

    checked = run(["-m", "alembic", "check"], database)
    assert checked.returncode == 0, checked.stderr

    # The baseline must produce a usable schema, not just tables.
    connection = sqlite3.connect(database)
    try:
        connection.execute(
            "INSERT INTO categories (name, description) VALUES ('Migration', 'test')"
        )
        connection.execute(
            "INSERT INTO products (name, sku, price, stock_quantity, reorder_level) "
            "VALUES ('Migrated product', 'MIG-1', 10.0, 3, 1)"
        )
        connection.commit()
        assert connection.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 1
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                "INSERT INTO products (name, sku, price, stock_quantity, reorder_level) "
                "VALUES ('Bad', 'MIG-2', -1, 0, 0)"
            )
    finally:
        connection.close()

    downgraded = run(["-m", "alembic", "downgrade", "base"], database)
    assert downgraded.returncode == 0, downgraded.stderr
    assert table_names(database).isdisjoint(
        {
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
    )


def test_empty_database_bootstrap_uses_alembic(tmp_path):
    database = tmp_path / "empty.db"

    result = run(["migrate.py"], database)
    assert result.returncode == 0, result.stderr
    assert scalar(database, "SELECT version_num FROM alembic_version") == "0001"
    assert "audit_logs" in table_names(database)
    assert "refresh_tokens" in table_names(database)


@pytest.mark.skipif(
    not LOCAL_DATABASE.is_file(),
    reason="No local development database to rehearse the unversioned upgrade",
)
def test_unversioned_database_upgrade_preserves_data(tmp_path):
    database = tmp_path / "legacy.db"
    shutil.copy2(LOCAL_DATABASE, database)

    tracked = [
        "users",
        "products",
        "orders",
        "suppliers",
        "purchase_orders",
        "inventory_transactions",
    ]
    before = {table: scalar(database, f"SELECT COUNT(*) FROM {table}") for table in tracked}

    result = run(["migrate.py"], database)
    assert result.returncode == 0, result.stderr

    after = {table: scalar(database, f"SELECT COUNT(*) FROM {table}") for table in tracked}
    assert after == before
    assert scalar(database, "SELECT version_num FROM alembic_version") == "0001"
    assert "audit_logs" in table_names(database)
    assert "refresh_tokens" in table_names(database)

    connection = sqlite3.connect(database)
    try:
        triggers = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'trigger'"
            )
        }
        assert "audit_logs_no_update" in triggers
        assert "products_integrity_insert" in triggers
    finally:
        connection.close()
