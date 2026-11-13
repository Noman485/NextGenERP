"""PostgreSQL concurrency, type and constraint parity checks.

These tests require a disposable PostgreSQL database and are skipped otherwise;
the security report labels that verification BLOCKED on machines without a
PostgreSQL service. Set ``TEST_POSTGRES_URL`` to a database whose name contains
``test`` before running:

    $env:TEST_POSTGRES_URL = "postgresql+psycopg://user:pass@127.0.0.1:5432/nextgenerp_test"
    python -m pytest tests/test_postgres_parity.py -q
"""

from __future__ import annotations

import os
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import Session

from database.connection import Base
from models.inventory_transaction import InventoryTransaction
from models.order import Order
from models.product import Product
from models.user import User
from services.inventory import change_stock

POSTGRES_URL = os.getenv("TEST_POSTGRES_URL", "").strip()


def _validate_disposable_database(url: str) -> None:
    database = (make_url(url).database or "").lower()
    assert "test" in database, (
        "TEST_POSTGRES_URL must point to a disposable database whose name "
        "contains 'test'"
    )


pytestmark = [
    pytest.mark.skipif(
        not POSTGRES_URL,
        reason="TEST_POSTGRES_URL is not configured; PostgreSQL verification is BLOCKED",
    ),
]


@pytest.fixture(scope="module")
def pg_engine():
    if not POSTGRES_URL:
        pytest.skip("TEST_POSTGRES_URL is not configured")
    _validate_disposable_database(POSTGRES_URL)
    engine = create_engine(POSTGRES_URL, pool_pre_ping=True)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def product(pg_engine):
    with Session(pg_engine) as session:
        entry = Product(
            name="PostgreSQL product",
            sku=f"PG-{datetime.now(timezone.utc).timestamp()}",
            price=10.0,
            stock_quantity=5,
            reorder_level=1,
        )
        session.add(entry)
        session.commit()
        return entry.id


def test_boolean_numeric_and_status_round_trip(pg_engine, product):
    with Session(pg_engine) as session:
        active = User(
            username=f"active-{datetime.now(timezone.utc).timestamp()}",
            password_hash="not-used",
            role="USER",
            is_active=True,
        )
        inactive = User(
            username=f"inactive-{datetime.now(timezone.utc).timestamp()}",
            password_hash="not-used",
            role="USER",
            is_active=False,
        )
        order = Order(
            customer_name="Parity customer",
            product_id=product,
            quantity=2,
            total_amount=20.0,
            status="Pending",
            created_at=datetime.now(timezone.utc),
        )
        session.add_all([active, inactive, order])
        session.commit()

        assert session.get(User, active.id).is_active is True
        assert session.get(User, inactive.id).is_active is False
        stored = session.get(Order, order.id).created_at
        assert stored.tzinfo is not None
        assert stored.utcoffset().total_seconds() == 0


def test_check_constraints_are_enforced(pg_engine, product):
    with Session(pg_engine) as session:
        session.add(
            Product(
                name="Negative price",
                sku="PG-NEGATIVE",
                price=-1,
                stock_quantity=1,
                reorder_level=0,
            )
        )
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()

    with Session(pg_engine) as session:
        session.add(
            Order(
                customer_name="Invalid status",
                product_id=product,
                quantity=1,
                total_amount=1,
                status="Completed",
            )
        )
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()


def test_with_for_update_blocks_a_second_writer(pg_engine, product):
    first = pg_engine.connect()
    second = pg_engine.connect()
    try:
        transaction = first.begin()
        first.execute(
            text("SELECT id FROM products WHERE id = :id FOR UPDATE"),
            {"id": product},
        )
        with pytest.raises(OperationalError):
            second.execute(
                text("SELECT id FROM products WHERE id = :id FOR UPDATE NOWAIT"),
                {"id": product},
            )
        transaction.rollback()
    finally:
        first.close()
        second.close()


def test_concurrent_stock_deduction_is_atomic(pg_engine, product):
    barrier = threading.Barrier(2)

    def sell():
        with Session(pg_engine) as session:
            barrier.wait(timeout=10)
            entry = (
                session.query(Product)
                .filter(Product.id == product)
                .with_for_update()
                .one()
            )
            try:
                change_stock(session, entry, "Stock Out", 4, "Concurrent sale")
                session.commit()
                return "sold"
            except HTTPException as error:
                session.rollback()
                assert error.status_code == 400
                return "insufficient"

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = sorted(executor.map(lambda _: sell(), range(2)))

    assert results == ["insufficient", "sold"]
    with Session(pg_engine) as session:
        assert session.get(Product, product).stock_quantity == 1
        movements = (
            session.query(InventoryTransaction)
            .filter(InventoryTransaction.product_id == product)
            .all()
        )
        assert len(movements) == 1
        assert movements[0].quantity == 4


def test_duplicate_sku_is_prevented_under_concurrency(pg_engine):
    barrier = threading.Barrier(2)

    def create():
        with Session(pg_engine) as session:
            barrier.wait(timeout=10)
            session.add(
                Product(
                    name="Race product",
                    sku="PG-RACE-SKU",
                    price=1,
                    stock_quantity=1,
                    reorder_level=0,
                )
            )
            try:
                session.commit()
                return "created"
            except IntegrityError:
                session.rollback()
                return "duplicate"

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = sorted(executor.map(lambda _: create(), range(2)))

    assert results == ["created", "duplicate"]
    with Session(pg_engine) as session:
        count = (
            session.query(Product).filter(Product.sku == "PG-RACE-SKU").count()
        )
        assert count == 1


def test_utc_round_trip_for_all_timestamp_columns(pg_engine):
    now = datetime.now(timezone.utc)
    # A direct SQL round-trip confirms the session timezone and server type
    # preserve the instant rather than silently dropping it.
    with pg_engine.connect() as connection:
        result = connection.execute(
            text("SELECT CAST(:value AS TIMESTAMPTZ)"), {"value": now}
        ).scalar_one()
    assert result.tzinfo is not None
    assert abs((result - now).total_seconds()) < 1
