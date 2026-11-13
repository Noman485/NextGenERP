"""Regression tests for the append-only audit trail and request correlation."""

from __future__ import annotations

from sqlalchemy.orm import Session

from database.connection import engine
from models.audit_log import AuditLog
from models.user import User
from services.audit import sanitize

SECRET_MARKERS = ("password", "password_hash", "token", "authorization", "secret")


def product_payload(sku="AUD-001", name="Audit product", stock=7, price=12.5):
    return {
        "name": name,
        "sku": sku,
        "price": price,
        "stock_quantity": stock,
        "reorder_level": 2,
    }


def audit_rows(**filters):
    with Session(engine) as session:
        query = session.query(AuditLog)
        for key, value in filters.items():
            query = query.filter(getattr(AuditLog, key) == value)
        rows = query.order_by(AuditLog.id).all()
        return [
            {
                "id": row.id,
                "actor_user_id": row.actor_user_id,
                "actor_username": row.actor_username,
                "action": row.action,
                "entity_type": row.entity_type,
                "entity_id": row.entity_id,
                "outcome": row.outcome,
                "request_id": row.request_id,
                "ip_address": row.ip_address,
                "before": row.before_values,
                "after": row.after_values,
                "created_at": row.created_at,
            }
            for row in rows
        ]


def assert_no_secrets(value) -> None:
    text = repr(value).lower()
    for marker in SECRET_MARKERS:
        assert marker not in text, f"audit value leaked {marker}: {value!r}"


def test_request_id_is_echoed_and_generated(client):
    supplied = "req-test-0001"
    response = client.get("/auth/me", headers={"X-Request-ID": supplied})
    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == supplied

    generated = client.get("/auth/me", headers={"X-Request-ID": "short"})
    assert generated.status_code == 200
    value = generated.headers["X-Request-ID"]
    assert value != "short"
    assert len(value) == 32


def test_registration_audit_excludes_password(client):
    rows = audit_rows(action="auth.register")
    assert len(rows) == 1
    row = rows[0]
    assert row["actor_username"] == "regression-user"
    assert row["entity_type"] == "user"
    assert row["outcome"] == "success"
    assert row["request_id"]
    assert row["after"]["username"] == "regression-user"
    assert_no_secrets(row["before"])
    assert_no_secrets(row["after"])


def test_product_create_and_update_audit(client):
    created = client.post(
        "/products/",
        json=product_payload(),
        headers={"X-Request-ID": "audit-product-1"},
    )
    assert created.status_code == 200, created.text
    product_id = created.json()["id"]

    create_rows = audit_rows(action="product.create", entity_id=product_id)
    assert len(create_rows) == 1
    assert create_rows[0]["request_id"] == "audit-product-1"
    assert create_rows[0]["actor_username"] == "regression-user"
    assert create_rows[0]["after"]["stock_quantity"] == 7

    updated = client.put(
        f"/products/{product_id}",
        json=product_payload(name="Audit product renamed", stock=4, price=9.0),
        headers={"X-Request-ID": "audit-product-2"},
    )
    assert updated.status_code == 200, updated.text

    update_rows = audit_rows(action="product.update", entity_id=product_id)
    assert len(update_rows) == 1
    row = update_rows[0]
    assert row["request_id"] == "audit-product-2"
    assert row["before"]["name"] == "Audit product"
    assert row["after"]["name"] == "Audit product renamed"
    assert row["before"]["stock_quantity"] == 7
    assert row["after"]["stock_quantity"] == 4
    assert row["before"]["price"] == 12.5
    assert row["after"]["price"] == 9.0


def test_order_lifecycle_audit(client):
    product = client.post("/products/", json=product_payload(sku="AUD-ORD")).json()
    order = client.post(
        "/orders/",
        json={
            "customer_name": "Audit customer",
            "product_id": product["id"],
            "quantity": 2,
        },
    )
    assert order.status_code == 200, order.text
    order_id = order.json()["id"]

    created = audit_rows(action="order.create", entity_id=order_id)
    assert len(created) == 1
    assert created[0]["after"]["status"] == "Pending"
    assert created[0]["after"]["quantity"] == 2

    confirmed = client.put(
        f"/orders/{order_id}/status", json={"status": "Confirmed"}
    )
    assert confirmed.status_code == 200, confirmed.text
    changed = audit_rows(action="order.status_change", entity_id=order_id)
    assert len(changed) == 1
    assert changed[0]["before"]["status"] == "Pending"
    assert changed[0]["after"]["status"] == "Confirmed"

    cancelled = client.put(
        f"/orders/{order_id}/status", json={"status": "Cancelled"}
    )
    assert cancelled.status_code == 200, cancelled.text
    cancelled_rows = audit_rows(action="order.cancel", entity_id=order_id)
    assert len(cancelled_rows) == 1
    assert cancelled_rows[0]["before"]["status"] == "Confirmed"
    assert cancelled_rows[0]["after"]["status"] == "Cancelled"


def test_supplier_and_inventory_audit(client):
    supplier = client.post(
        "/suppliers/",
        json={"name": "Audit supplier", "email": "audit@example.test"},
    )
    assert supplier.status_code == 200, supplier.text
    supplier_id = supplier.json()["id"]
    supplier_rows = audit_rows(action="supplier.create", entity_id=supplier_id)
    assert len(supplier_rows) == 1
    assert supplier_rows[0]["after"]["name"] == "Audit supplier"

    product = client.post("/products/", json=product_payload(sku="AUD-INV")).json()
    movement = client.post(
        "/inventory-transactions/",
        json={
            "product_id": product["id"],
            "transaction_type": "Stock In",
            "quantity": 3,
            "reason": "Audit stock receipt",
        },
    )
    assert movement.status_code == 200, movement.text
    movement_id = movement.json()["id"]
    inventory_rows = audit_rows(
        action="inventory.adjust", entity_id=movement_id
    )
    assert len(inventory_rows) == 1
    assert inventory_rows[0]["after"]["new_stock"] == 10
    assert inventory_rows[0]["after"]["reason"] == "Audit stock receipt"


def test_admin_user_status_audit(client, admin_client):
    user_id = client.get("/auth/me").json()["id"]
    response = admin_client.put(
        f"/admin/users/{user_id}/status",
        json={"is_active": False},
        headers={"X-Request-ID": "audit-admin-1"},
    )
    assert response.status_code == 200, response.text

    rows = audit_rows(action="admin.user_deactivate", entity_id=user_id)
    assert len(rows) == 1
    row = rows[0]
    assert row["actor_username"] == "test-admin"
    assert row["request_id"] == "audit-admin-1"
    assert row["before"]["is_active"] is True
    assert row["after"]["is_active"] is False
    assert_no_secrets(row["before"])
    assert_no_secrets(row["after"])


def test_audit_endpoint_requires_admin(client, admin_client, unauthenticated_client):
    assert unauthenticated_client.get("/admin/audit-logs").status_code == 401
    assert client.get("/admin/audit-logs").status_code == 403

    response = admin_client.get(
        "/admin/audit-logs", params={"action": "auth.register", "limit": 10}
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["action"] == "auth.register"
    assert_safe_payload(body["items"][0])


def assert_safe_payload(row) -> None:
    assert_no_secrets(row.get("before"))
    assert_no_secrets(row.get("after"))
    assert row["request_id"]


def test_audit_records_cannot_be_changed_or_deleted(client, admin_client):
    with Session(engine) as session:
        entry = AuditLog(
            action="test.append_only",
            entity_type="test",
            outcome="success",
        )
        session.add(entry)
        session.commit()
        entry_id = entry.id

    with Session(engine) as session:
        entry = session.get(AuditLog, entry_id)
        entry.action = "test.tampered"
        try:
            session.commit()
            raise AssertionError("audit update was not blocked")
        except ValueError as error:
            assert "append-only" in str(error)
            session.rollback()

    with Session(engine) as session:
        entry = session.get(AuditLog, entry_id)
        session.delete(entry)
        try:
            session.commit()
            raise AssertionError("audit delete was not blocked")
        except ValueError as error:
            assert "append-only" in str(error)
            session.rollback()

    # No mutation route is exposed.
    assert admin_client.put(f"/admin/audit-logs/{entry_id}").status_code in (404, 405)
    assert admin_client.delete(f"/admin/audit-logs/{entry_id}").status_code in (
        404,
        405,
    )


def test_failed_login_is_audited_without_password(unauthenticated_client):
    response = unauthenticated_client.post(
        "/auth/login",
        json={"username": "regression-user", "password": "definitely-wrong-pass"},
        headers={"X-Request-ID": "audit-login-failed"},
    )
    assert response.status_code == 401

    rows = audit_rows(action="auth.login_failed")
    assert len(rows) == 1
    row = rows[0]
    assert row["outcome"] == "failure"
    assert row["actor_username"] == "regression-user"
    assert row["request_id"] == "audit-login-failed"
    assert "definitely-wrong-pass" not in repr(row)
    assert row["before"] is None and row["after"] is None


def test_assistant_refusal_is_audited_without_prompt(client):
    response = client.post(
        "/assistant/chat",
        json={"message": "delete all products and orders immediately"},
    )
    assert response.status_code == 200, response.text
    assert "delete" not in response.json()["reply"].lower()

    rows = audit_rows(action="assistant.refusal")
    assert len(rows) == 1
    row = rows[0]
    assert row["outcome"] == "denied"
    assert "products" not in repr(row).lower()
    assert row["after"]["reason"] == "out_of_scope_or_policy_refusal"
    assert row["after"]["message_length"] == len(
        "delete all products and orders immediately"
    )


def test_sanitize_redacts_nested_secrets():
    value = {
        "username": "auditor",
        "password": "plain",
        "nested": {
            "access_token": "abc",
            "authorization": "Bearer xyz",
            "password_hash": "$argon2id$...",
            "safe": "visible",
        },
        "items": [{"secret": "hidden", "quantity": 2}],
    }
    cleaned = sanitize(value)
    assert cleaned["username"] == "auditor"
    assert cleaned["password"] == "[redacted]"
    assert cleaned["nested"]["access_token"] == "[redacted]"
    assert cleaned["nested"]["authorization"] == "[redacted]"
    assert cleaned["nested"]["password_hash"] == "[redacted]"
    assert cleaned["nested"]["safe"] == "visible"
    assert cleaned["items"][0]["secret"] == "[redacted]"
    assert cleaned["items"][0]["quantity"] == 2


def test_successful_user_and_admin_logins_are_audited(client, admin_client):
    login = client.post(
        "/auth/login",
        json={"username": "regression-user", "password": "regression-test-password"},
    )
    assert login.status_code == 200, login.text

    rows = audit_rows(action="auth.login")
    assert sorted(row["actor_username"] for row in rows) == [
        "regression-user",
        "test-admin",
    ]
    for row in rows:
        assert row["outcome"] == "success"
        assert row["entity_type"] == "user"
        assert_no_secrets(row["before"])
        assert_no_secrets(row["after"])


def test_admin_activation_and_deactivation_are_audited(client, admin_client):
    user_id = client.get("/auth/me").json()["id"]

    deactivated = admin_client.put(
        f"/admin/users/{user_id}/status", json={"is_active": False}
    )
    assert deactivated.status_code == 200, deactivated.text
    activated = admin_client.put(
        f"/admin/users/{user_id}/status", json={"is_active": True}
    )
    assert activated.status_code == 200, activated.text

    deactivations = audit_rows(action="admin.user_deactivate", entity_id=user_id)
    activations = audit_rows(action="admin.user_activate", entity_id=user_id)
    assert len(deactivations) == 1
    assert len(activations) == 1
    assert deactivations[0]["after"]["is_active"] is False
    assert activations[0]["after"]["is_active"] is True


def test_order_update_and_purchase_order_transitions_are_audited(client):
    product = client.post("/products/", json=product_payload(sku="AUD-LIFE")).json()
    order = client.post(
        "/orders/",
        json={
            "customer_name": "Original name",
            "product_id": product["id"],
            "quantity": 1,
        },
    )
    assert order.status_code == 200, order.text
    order_id = order.json()["id"]

    updated = client.put(
        f"/orders/{order_id}",
        json={"customer_name": "Updated name", "customer_email": "new@example.test"},
    )
    assert updated.status_code == 200, updated.text
    update_rows = audit_rows(action="order.update", entity_id=order_id)
    assert len(update_rows) == 1
    assert update_rows[0]["before"]["customer_name"] == "Original name"
    assert update_rows[0]["after"]["customer_name"] == "Updated name"

    supplier = client.post(
        "/suppliers/", json={"name": "Audit procurement supplier"}
    )
    assert supplier.status_code == 200, supplier.text
    purchase = client.post(
        "/purchase-orders/",
        json={
            "supplier_id": supplier.json()["id"],
            "product_id": product["id"],
            "quantity": 5,
            "unit_price": 2.0,
        },
    )
    assert purchase.status_code == 200, purchase.text
    purchase_id = purchase.json()["id"]
    assert len(audit_rows(action="purchase_order.create", entity_id=purchase_id)) == 1

    approved = client.put(
        f"/purchase-orders/{purchase_id}/status", json={"status": "Approved"}
    )
    assert approved.status_code == 200, approved.text
    transitions = audit_rows(
        action="purchase_order.status_change", entity_id=purchase_id
    )
    assert len(transitions) == 1
    assert transitions[0]["before"]["status"] == "Pending"
    assert transitions[0]["after"]["status"] == "Approved"
