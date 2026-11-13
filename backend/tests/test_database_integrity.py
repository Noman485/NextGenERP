"""Database integrity tests for Phase 2.

The tests exercise the real SQLite schema used by the test suite. PostgreSQL
concurrency and migration verification cannot run without a PostgreSQL service
and remain BLOCKED in the security report.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from sqlalchemy import inspect, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth.tokens import normalize_utc
from database.connection import engine
from database.migrations import ensure_schema
from models.order import Order
from models.product import Product
from models.purchase_order import PurchaseOrder
from models.supplier import Supplier
from models.user import User

PRODUCT_CONSTRAINTS = {
    "ck_products_price_non_negative",
    "ck_products_stock_non_negative",
    "ck_products_reorder_non_negative",
}
ORDER_CONSTRAINTS = {
    "ck_orders_quantity_positive",
    "ck_orders_total_non_negative",
    "ck_orders_status_valid",
}
PURCHASE_ORDER_CONSTRAINTS = {
    "ck_purchase_orders_quantity_positive",
    "ck_purchase_orders_unit_price_non_negative",
    "ck_purchase_orders_total_non_negative",
    "ck_purchase_orders_status_valid",
}
SUPPLIER_CONSTRAINTS = {
    "ck_suppliers_lead_time_non_negative",
    "ck_suppliers_rating_range",
}


def constraint_names(table: str) -> set[str]:
    inspector = inspect(engine)
    return {
        constraint["name"]
        for constraint in inspector.get_check_constraints(table)
        if constraint.get("name")
    }


def insert_user_and_product(stock: int = 10) -> int:
    with Session(engine) as session:
        user = User(
            username="integrity-user",
            password_hash="not-used",
            role="USER",
            is_active=True,
        )
        product = Product(
            name="Integrity product",
            sku="INTEGRITY-1",
            price=10.0,
            stock_quantity=stock,
            reorder_level=1,
        )
        session.add_all([user, product])
        session.commit()
        return product.id


def expect_integrity_error(statement: str, parameters: dict) -> None:
    with pytest.raises(IntegrityError):
        with engine.begin() as connection:
            connection.execute(text(statement), parameters)


def test_fresh_schema_declares_integrity_constraints():
    assert PRODUCT_CONSTRAINTS <= constraint_names("products")
    assert ORDER_CONSTRAINTS <= constraint_names("orders")
    assert PURCHASE_ORDER_CONSTRAINTS <= constraint_names("purchase_orders")
    assert SUPPLIER_CONSTRAINTS <= constraint_names("suppliers")


def test_product_rejects_negative_price_and_stock():
    with Session(engine) as session:
        session.add(
            Product(
                name="Negative price",
                sku="NEG-PRICE",
                price=-0.01,
                stock_quantity=1,
                reorder_level=0,
            )
        )
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()

    with Session(engine) as session:
        session.add(
            Product(
                name="Negative stock",
                sku="NEG-STOCK",
                price=1.0,
                stock_quantity=-1,
                reorder_level=0,
            )
        )
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()


def test_order_rejects_invalid_quantity_and_status():
    product_id = insert_user_and_product()
    user_id = 1

    expect_integrity_error(
        "INSERT INTO orders (customer_name, product_id, quantity, total_amount, status, user_id) "
        "VALUES (:name, :product_id, :quantity, :total, :status, :user_id)",
        {
            "name": "Bad quantity",
            "product_id": product_id,
            "quantity": 0,
            "total": 0,
            "status": "Pending",
            "user_id": user_id,
        },
    )
    expect_integrity_error(
        "INSERT INTO orders (customer_name, product_id, quantity, total_amount, status, user_id) "
        "VALUES (:name, :product_id, :quantity, :total, :status, :user_id)",
        {
            "name": "Bad status",
            "product_id": product_id,
            "quantity": 1,
            "total": 10,
            "status": "Completed",
            "user_id": user_id,
        },
    )


def test_purchase_order_rejects_invalid_values():
    product_id = insert_user_and_product()
    with Session(engine) as session:
        session.add(
            Supplier(
                name="Integrity supplier",
                lead_time_days=1,
                performance_rating=3.0,
            )
        )
        session.commit()
        supplier_id = session.query(Supplier).one().id

    expect_integrity_error(
        "INSERT INTO purchase_orders "
        "(supplier_id, product_id, quantity, unit_price, total_amount, status) "
        "VALUES (:supplier_id, :product_id, :quantity, :unit_price, :total, :status)",
        {
            "supplier_id": supplier_id,
            "product_id": product_id,
            "quantity": 1,
            "unit_price": -1,
            "total": -1,
            "status": "Pending",
        },
    )
    expect_integrity_error(
        "INSERT INTO purchase_orders "
        "(supplier_id, product_id, quantity, unit_price, total_amount, status) "
        "VALUES (:supplier_id, :product_id, :quantity, :unit_price, :total, :status)",
        {
            "supplier_id": supplier_id,
            "product_id": product_id,
            "quantity": 1,
            "unit_price": 5,
            "total": 5,
            "status": "Completed",
        },
    )


def test_supplier_rejects_negative_lead_time_and_out_of_range_rating():
    with Session(engine) as session:
        session.add(
            Supplier(
                name="Bad lead time",
                lead_time_days=-1,
                performance_rating=None,
            )
        )
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()

    with Session(engine) as session:
        session.add(
            Supplier(
                name="Bad rating",
                lead_time_days=1,
                performance_rating=5.01,
            )
        )
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()


def test_duplicate_sku_is_rejected_without_partial_rows(client):
    first = client.post(
        "/products/",
        json={
            "name": "Unique product",
            "sku": "DUPLICATE-SKU",
            "price": 5.0,
            "stock_quantity": 2,
            "reorder_level": 1,
        },
    )
    assert first.status_code == 200, first.text

    duplicate = client.post(
        "/products/",
        json={
            "name": "Duplicate product",
            "sku": "DUPLICATE-SKU",
            "price": 6.0,
            "stock_quantity": 2,
            "reorder_level": 1,
        },
    )
    assert duplicate.status_code == 409

    with Session(engine) as session:
        assert session.query(Product).filter(Product.sku == "DUPLICATE-SKU").count() == 1
        assert session.query(Product).count() == 1


def test_insufficient_stock_rolls_back_order_and_stock(client):
    product = client.post(
        "/products/",
        json={
            "name": "Scarce product",
            "sku": "SCARCE-1",
            "price": 9.0,
            "stock_quantity": 1,
            "reorder_level": 0,
        },
    )
    assert product.status_code == 200, product.text
    product_id = product.json()["id"]

    response = client.post(
        "/orders/",
        json={
            "customer_name": "Atomic customer",
            "product_id": product_id,
            "quantity": 2,
        },
    )
    assert response.status_code == 400

    with Session(engine) as session:
        assert session.query(Order).count() == 0
        stored = session.get(Product, product_id)
        assert stored.stock_quantity == 1


def test_successful_order_commits_order_stock_and_audit_together(client):
    product = client.post(
        "/products/",
        json={
            "name": "Ordered product",
            "sku": "ORDERED-1",
            "price": 4.5,
            "stock_quantity": 6,
            "reorder_level": 0,
        },
    )
    assert product.status_code == 200, product.text
    product_id = product.json()["id"]

    response = client.post(
        "/orders/",
        json={
            "customer_name": "Atomic customer",
            "customer_email": "atomic@example.test",
            "product_id": product_id,
            "quantity": 2,
        },
    )
    assert response.status_code == 200, response.text
    order_id = response.json()["id"]

    with Session(engine) as session:
        order = session.get(Order, order_id)
        assert order is not None
        assert order.quantity == 2
        assert float(order.total_amount) == 9.0
        assert session.get(Product, product_id).stock_quantity == 4
        movements = session.execute(
            text(
                "SELECT quantity, previous_stock, new_stock FROM inventory_transactions "
                "WHERE product_id = :product_id ORDER BY id"
            ),
            {"product_id": product_id},
        ).all()
        # The first movement records the initial stock, the second the sale.
        assert movements[-1] == (2, 6, 4)
        audit_count = session.execute(
            text(
                "SELECT COUNT(*) FROM audit_logs WHERE action = 'order.create' "
                "AND entity_id = :order_id"
            ),
            {"order_id": order_id},
        ).scalar_one()
        assert audit_count == 1


def test_legacy_sqlite_database_gains_enforcement_triggers():
    ensure_schema()
    with engine.begin() as connection:
        triggers = {
            row[0]
            for row in connection.execute(
                text("SELECT name FROM sqlite_master WHERE type = 'trigger'")
            )
        }
    assert {
        "products_integrity_insert",
        "products_integrity_update",
        "orders_integrity_insert",
        "orders_integrity_update",
        "purchase_orders_integrity_insert",
        "purchase_orders_integrity_update",
        "suppliers_integrity_insert",
        "suppliers_integrity_update",
    } <= triggers

    product_id = insert_user_and_product()
    expect_integrity_error(
        "INSERT INTO orders (customer_name, product_id, quantity, total_amount, status) "
        "VALUES ('Triggered', :product_id, 1, -5, 'Pending')",
        {"product_id": product_id},
    )


def test_sqlite_utc_datetime_round_trip(client):
    product = client.post(
        "/products/",
        json={
            "name": "UTC product",
            "sku": "UTC-1",
            "price": 1.0,
            "stock_quantity": 1,
            "reorder_level": 0,
        },
    ).json()
    created = client.post(
        "/orders/",
        json={
            "customer_name": "UTC customer",
            "product_id": product["id"],
            "quantity": 1,
        },
    )
    assert created.status_code == 200, created.text

    with Session(engine) as session:
        stored = session.get(Order, created.json()["id"]).created_at
    normalized = normalize_utc(stored)
    assert normalized is not None
    delta = abs((datetime.now(timezone.utc) - normalized).total_seconds())
    assert delta < 120
