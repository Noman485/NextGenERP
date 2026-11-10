from datetime import datetime, timezone

import jwt
import pytest
from sqlalchemy.orm import Session

from admin_provision import provision_admin
from database.connection import engine
from models.order import Order
from models.user import User

TEST_SECRET = "test-only-secret-key-never-use-outside-tests"


def submit_order(client, product_id, quantity=2):
    response = client.post(
        "/orders/",
        json={
            "customer_name": "Analytics customer",
            "customer_email": "analytics@example.test",
            "product_id": product_id,
            "quantity": quantity,
        },
    )
    assert response.status_code == 200, response.text
    return response.json()


def set_status(client, order_id, status):
    response = client.put(f"/orders/{order_id}/status", json={"status": status})
    assert response.status_code == 200, response.text
    return response.json()


def create_sales_fixture(client, create_product):
    product = create_product(stock_quantity=100)
    pending = submit_order(client, product["id"], 2)
    confirmed = submit_order(client, product["id"], 3)
    set_status(client, confirmed["id"], "Confirmed")
    delivered = submit_order(client, product["id"], 1)
    set_status(client, delivered["id"], "Confirmed")
    set_status(client, delivered["id"], "Shipped")
    set_status(client, delivered["id"], "Delivered")
    cancelled = submit_order(client, product["id"], 2)
    set_status(client, cancelled["id"], "Cancelled")
    return product, [pending, confirmed, delivered, cancelled]


def test_admin_routes_require_an_active_administrator(client, admin_client):
    assert client.get("/admin/overview").status_code == 403
    assert client.get("/admin/users").status_code == 403
    assert client.get("/admin/analytics/daily").status_code == 403
    assert admin_client.get("/admin/overview").status_code == 200
    assert admin_client.get("/admin/users").status_code == 200


def test_unauthenticated_admin_routes_return_401(unauthenticated_client):
    for path in (
        "/admin/overview",
        "/admin/users",
        "/admin/analytics/daily",
        "/admin/analytics/monthly",
        "/admin/analytics/yearly",
        "/admin/analytics/products",
        "/admin/analytics/inventory",
        "/admin/analytics/suppliers",
    ):
        assert unauthenticated_client.get(path).status_code == 401


def test_admin_overview_uses_realized_revenue_and_excludes_pending_and_cancelled(
    client,
    admin_client,
    create_product,
    create_supplier,
):
    product, _ = create_sales_fixture(client, create_product)
    supplier = create_supplier()

    received = client.post(
        "/purchase-orders/",
        json={
            "supplier_id": supplier["id"],
            "product_id": product["id"],
            "quantity": 10,
            "unit_price": 2,
        },
    ).json()
    assert client.put(
        f"/purchase-orders/{received['id']}/status",
        json={"status": "Approved"},
    ).status_code == 200
    assert client.put(
        f"/purchase-orders/{received['id']}/status",
        json={"status": "Received"},
    ).status_code == 200

    pending_purchase = client.post(
        "/purchase-orders/",
        json={
            "supplier_id": supplier["id"],
            "product_id": product["id"],
            "quantity": 5,
            "unit_price": 2,
        },
    )
    assert pending_purchase.status_code == 200

    overview = admin_client.get("/admin/overview").json()
    assert overview["total_orders"] == 4
    assert overview["pending_orders"] == 1
    assert overview["confirmed_orders"] == 1
    assert overview["completed_orders"] == 1
    assert overview["cancelled_orders"] == 1
    assert overview["total_sales"] == 2
    assert overview["total_sales_revenue"] == 50.0
    assert overview["pipeline_revenue"] == 25.0
    assert overview["cancelled_value"] == 25.0
    assert overview["average_order_value"] == 25.0
    assert overview["total_products"] == 1
    assert overview["total_suppliers"] == 1
    assert overview["total_inventory_units"] == 104
    assert overview["inventory_value_at_selling_price"] == 1300.0
    assert overview["purchase_orders"] == 2
    assert overview["received_purchase_orders"] == 1
    assert overview["pending_purchase_orders"] == 1
    assert overview["purchase_expenditure"] == 20.0
    assert overview["pending_purchase_value"] == 10.0


def test_daily_monthly_and_yearly_series_are_consistent(
    client,
    admin_client,
    create_product,
):
    create_sales_fixture(client, create_product)

    daily = admin_client.get("/admin/analytics/daily?days=30").json()
    assert len(daily["series"]) == 30
    assert daily["totals"]["orders"] == 4
    assert daily["totals"]["revenue"] == 50.0
    assert daily["totals"]["completed_orders"] == 1
    assert daily["totals"]["cancelled_orders"] == 1
    assert daily["totals"]["average_order_value"] == 25.0
    assert daily["series"][-1]["orders"] == 4
    assert daily["series"][-1]["revenue"] == 50.0

    monthly = admin_client.get("/admin/analytics/monthly").json()
    assert len(monthly["series"]) == 12
    assert monthly["totals"]["orders"] == 4
    assert monthly["totals"]["revenue"] == 50.0
    assert sum(month["orders"] for month in monthly["series"]) == 4
    assert sum(month["revenue"] for month in monthly["series"]) == 50.0

    yearly = admin_client.get("/admin/analytics/yearly?years=5").json()
    assert len(yearly["series"]) == 5
    assert yearly["totals"]["orders"] == 4
    assert yearly["totals"]["revenue"] == 50.0
    assert yearly["series"][-1]["year"] == datetime.now(timezone.utc).year


def test_monthly_analytics_handles_historical_orders_and_missing_months(
    client,
    admin_client,
    create_product,
):
    product = create_product(stock_quantity=100)
    order = submit_order(client, product["id"], 2)
    assert set_status(client, order["id"], "Confirmed")["status"] == "Confirmed"
    with Session(engine) as session:
        stored = session.get(Order, order["id"])
        stored.created_at = datetime(2024, 2, 10, 12, 0, tzinfo=timezone.utc)
        session.commit()

    monthly = admin_client.get("/admin/analytics/monthly?year=2024").json()
    assert monthly["year"] == 2024
    february = next(item for item in monthly["series"] if item["month"] == 2)
    january = next(item for item in monthly["series"] if item["month"] == 1)
    assert february["orders"] == 1
    assert february["revenue"] == 25.0
    assert january["orders"] == 0
    assert january["revenue"] == 0.0
    assert february["previous_month_growth_percent"] == 100.0

    yearly = admin_client.get("/admin/analytics/yearly?years=5").json()
    assert 2024 in [item["year"] for item in yearly["series"]]
    year_2024 = next(item for item in yearly["series"] if item["year"] == 2024)
    assert year_2024["orders"] == 1
    assert year_2024["revenue"] == 25.0


def test_user_product_and_supplier_analytics(
    client,
    admin_client,
    create_product,
    create_supplier,
):
    product, _ = create_sales_fixture(client, create_product)
    supplier = create_supplier()
    purchase = client.post(
        "/purchase-orders/",
        json={
            "supplier_id": supplier["id"],
            "product_id": product["id"],
            "quantity": 4,
            "unit_price": 2.5,
        },
    ).json()
    assert client.put(
        f"/purchase-orders/{purchase['id']}/status",
        json={"status": "Approved"},
    ).status_code == 200
    assert client.put(
        f"/purchase-orders/{purchase['id']}/status",
        json={"status": "Received"},
    ).status_code == 200

    users = admin_client.get("/admin/analytics/users").json()
    normal = next(
        item for item in users["items"] if item["username"] == "regression-user"
    )
    assert normal["orders"] == 4
    assert normal["realized_orders"] == 2
    assert normal["completed_orders"] == 1
    assert normal["cancelled_orders"] == 1
    assert normal["revenue"] == 50.0
    assert normal["average_order_value"] == 25.0

    products = admin_client.get("/admin/analytics/products").json()
    assert products["total"] == 1
    item = products["items"][0]
    assert item["product_id"] == product["id"]
    assert item["orders"] == 4
    assert item["units_sold"] == 6
    assert item["realized_units"] == 4
    assert item["revenue"] == 50.0
    assert item["stock_quantity"] == 98
    assert item["slow_moving_last_30_days"] is False
    assert products["best_sellers"][0]["product_id"] == product["id"]

    suppliers = admin_client.get("/admin/analytics/suppliers").json()
    assert suppliers["total"] == 1
    supplier_row = suppliers["items"][0]
    assert supplier_row["purchase_orders"] == 1
    assert supplier_row["received_purchases"] == 1
    assert supplier_row["purchase_expenditure"] == 10.0
    assert supplier_row["pending_value"] == 0.0


def test_inventory_analytics_matches_stock_and_movements(
    client,
    admin_client,
    create_product,
):
    create_sales_fixture(client, create_product)
    inventory = admin_client.get("/admin/analytics/inventory").json()
    assert inventory["total_products"] == 1
    assert inventory["total_units"] == 94
    assert inventory["inventory_value_at_selling_price"] == 1175.0
    assert inventory["low_stock_count"] == 0
    assert inventory["out_of_stock_count"] == 0
    assert inventory["stock_movements_last_30_days"]["stock_out_units"] == 8
    assert inventory["stock_movements_last_30_days"]["stock_in_units"] == 102
    assert inventory["recent_movements"][0]["transaction_type"] in {
        "Stock In",
        "Stock Out",
    }


def test_admin_user_listing_and_detail_never_expose_password_hashes(
    client,
    admin_client,
):
    users = admin_client.get("/admin/users").json()
    normal = next(
        item for item in users["items"] if item["username"] == "regression-user"
    )
    assert "password_hash" not in normal
    assert normal["role"] == "USER"
    assert normal["is_active"] is True
    assert normal["email"] is None

    detail = admin_client.get(f"/admin/users/{normal['user_id']}").json()
    assert detail["user"]["username"] == "regression-user"
    assert "password_hash" not in detail["user"]
    assert detail["sales_summary"]["orders"] == 0


def test_admin_can_deactivate_a_user_but_not_self(
    client,
    admin_client,
):
    me = client.get("/auth/me").json()
    deactivated = admin_client.put(
        f"/admin/users/{me['id']}/status",
        json={"is_active": False},
    )
    assert deactivated.status_code == 200
    assert deactivated.json()["is_active"] is False
    assert client.get("/auth/me").status_code == 403
    assert client.post(
        "/auth/login",
        json={
            "username": "regression-user",
            "password": "regression-test-password",
        },
    ).status_code == 403

    admin = admin_client.get("/auth/me").json()
    self_deactivation = admin_client.put(
        f"/admin/users/{admin['id']}/status",
        json={"is_active": False},
    )
    assert self_deactivation.status_code == 400
    assert "own administrator" in self_deactivation.json()["detail"]


def test_status_update_cannot_escalate_a_user_role(client, admin_client):
    me = client.get("/auth/me").json()
    response = admin_client.put(
        f"/admin/users/{me['id']}/status",
        json={"is_active": True, "role": "ADMIN"},
    )
    assert response.status_code == 200
    assert response.json()["role"] == "USER"
    with Session(engine) as session:
        assert session.get(User, me["id"]).role == "USER"


def test_registration_defaults_to_user_and_token_has_no_role_claim(
    unauthenticated_client,
):
    response = unauthenticated_client.post(
        "/auth/register",
        json={
            "username": "role-user",
            "password": "long-test-password-123",
            "email": "Role-User@Example.Test",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["user"]["role"] == "USER"
    assert data["user"]["email"] == "role-user@example.test"
    payload = jwt.decode(
        data["access_token"],
        TEST_SECRET,
        algorithms=["HS256"],
    )
    assert "role" not in payload
    assert payload["sub"] == str(data["user"]["id"])


def test_provisioning_never_promotes_an_existing_user_implicitly(client):
    with Session(engine) as session:
        with pytest.raises(ValueError, match="normal user"):
            provision_admin(
                session,
                "regression-user",
                "another-long-password-123",
            )
        result = provision_admin(
            session,
            "regression-user",
            "another-long-password-123",
            promote=True,
        )
        assert result.created is False
        assert result.user.role == "ADMIN"


def test_admin_analytics_handle_an_empty_database(admin_client):
    overview = admin_client.get("/admin/overview").json()
    assert overview["total_orders"] == 0
    assert overview["total_sales_revenue"] == 0.0
    assert overview["average_order_value"] == 0.0

    daily = admin_client.get("/admin/analytics/daily?days=7").json()
    assert len(daily["series"]) == 7
    assert all(item["orders"] == 0 for item in daily["series"])
    monthly = admin_client.get("/admin/analytics/monthly").json()
    assert len(monthly["series"]) == 12
    yearly = admin_client.get("/admin/analytics/yearly").json()
    assert len(yearly["series"]) == 5


def test_money_rounding_uses_two_decimal_places():
    from services.analytics import money

    assert money(10.005) == 10.01
    assert money(None) == 0.0
    assert money("12.345") == 12.35
