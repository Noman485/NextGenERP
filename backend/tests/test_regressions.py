import pandas as pd
import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


def submit_order(client, product_id, quantity=2):
    return client.post(
        "/orders/",
        json={
            "customer_name": "Original Customer",
            "customer_email": "original@example.test",
            "product_id": product_id,
            "quantity": quantity,
        },
    )


def test_order_update_trims_customer_fields_and_rejects_blank_name(
    client,
    create_product,
):
    product = create_product()
    order = submit_order(client, product["id"]).json()

    updated = client.put(
        f"/orders/{order['id']}",
        json={
            "customer_name": "  Updated Customer  ",
            "customer_email": "  updated@example.test  ",
        },
    )
    assert updated.status_code == 200
    assert updated.json()["customer_name"] == "Updated Customer"
    assert updated.json()["customer_email"] == "updated@example.test"

    blank_name = client.put(
        f"/orders/{order['id']}",
        json={"customer_name": "   ", "customer_email": None},
    )
    assert blank_name.status_code == 400

    cleared_email = client.put(
        f"/orders/{order['id']}",
        json={"customer_name": "Updated Customer", "customer_email": "   "},
    )
    assert cleared_email.status_code == 200
    assert cleared_email.json()["customer_email"] is None

    persisted = client.get("/orders/").json()[0]
    assert persisted["customer_name"] == "Updated Customer"
    assert persisted["customer_email"] is None


def test_ml_insights_generates_forecast_once_and_matches_erp_case_insensitively(
    client,
    create_product,
    monkeypatch,
):
    import routes.ml as ml_routes

    product = create_product(
        name="Amul Butter",
        sku="AMUL-1",
        stock_quantity=5,
        reorder_level=2,
    )
    calls = {"forecast": 0}
    captured = {}

    def fake_generate_forecast():
        calls["forecast"] += 1
        return pd.DataFrame(
            {
                "product": ["amul butter", "Unmatched Item"],
                "product_id": [101, 102],
            }
        )

    def fake_load_inventory():
        return {
            101: {"stock": 999, "lead_time": 4, "supplier": "Fallback A"},
            102: {"stock": 7, "lead_time": 6, "supplier": "Fallback B"},
        }

    def fake_get_ml_results(inventory=None, forecast_df=None):
        captured["inventory"] = inventory
        captured["forecast_df"] = forecast_df
        return {
            "recommendations": [
                {"product": "amul butter", "product_id": 101},
                {"product": "Unmatched Item", "product_id": 102},
            ]
        }

    monkeypatch.setattr(ml_routes, "generate_forecast", fake_generate_forecast)
    monkeypatch.setattr(ml_routes, "load_inventory", fake_load_inventory)
    monkeypatch.setattr(ml_routes, "get_ml_results", fake_get_ml_results)

    response = client.get("/ml/insights")
    assert response.status_code == 200
    assert calls["forecast"] == 1
    assert captured["forecast_df"] is not None

    inventory = captured["inventory"]
    assert inventory[101]["stock"] == 5
    assert inventory[102]["stock"] == 7

    recommendations = {
        item["product"]: item for item in response.json()["recommendations"]
    }
    assert recommendations["amul butter"]["erp_product_id"] == product["id"]
    assert recommendations["amul butter"]["erp_sku"] == "AMUL-1"
    assert recommendations["amul butter"]["erp_reorder_level"] == 2
    assert recommendations["Unmatched Item"]["erp_product_id"] is None
    assert recommendations["Unmatched Item"]["erp_sku"] is None


@pytest.mark.parametrize("method", ["post", "put", "delete"])
def test_supplier_commit_failures_return_service_unavailable(
    client,
    create_supplier,
    monkeypatch,
    method,
):
    supplier = create_supplier()

    def fail_commit(_session):
        raise SQLAlchemyError("simulated database failure")

    monkeypatch.setattr(Session, "commit", fail_commit)

    if method == "post":
        response = client.post(
            "/suppliers/",
            json={"name": "New supplier", "lead_time_days": 2},
        )
    elif method == "put":
        response = client.put(
            f"/suppliers/{supplier['id']}",
            json={"name": "Updated supplier", "lead_time_days": 2},
        )
    else:
        response = client.delete(f"/suppliers/{supplier['id']}")

    assert response.status_code == 503
    assert response.json()["detail"].startswith("Unable to")
