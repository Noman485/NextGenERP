import requests


def ask(client, message, history=None):
    return client.post(
        "/assistant/chat",
        json={"message": message, "history": history or []},
    )


def test_assistant_requires_authentication(unauthenticated_client):
    response = unauthenticated_client.post(
        "/assistant/chat",
        json={"message": "hello"},
    )
    assert response.status_code == 401


def test_assistant_rejects_blank_oversized_and_long_history(client):
    assert ask(client, "   ").status_code == 422
    assert ask(client, "x" * 1001).status_code == 422
    assert ask(
        client,
        "hello",
        history=[{"role": "user", "content": "hi"}] * 11,
    ).status_code == 422


def test_assistant_greeting_is_project_scoped(client):
    response = ask(client, "hello")
    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "local"
    assert "NextGenERP" in data["reply"]
    assert data["suggestions"]


def test_assistant_refuses_off_topic_questions(client):
    response = ask(client, "Who won the cricket world cup?")
    assert response.status_code == 200
    reply = response.json()["reply"]
    assert "only help with NextGenERP" in reply
    assert "cricket" not in reply.lower()


def test_assistant_answers_low_stock_from_live_data(client, create_product):
    create_product(
        name="Healthy Widget",
        sku="HEALTHY-1",
        stock_quantity=50,
        reorder_level=5,
    )
    create_product(
        name="Low Widget",
        sku="LOW-1",
        stock_quantity=2,
        reorder_level=5,
    )

    response = ask(client, "Which products are low on stock?")
    assert response.status_code == 200
    reply = response.json()["reply"]
    assert "Low Widget" in reply
    assert "Healthy Widget" not in reply
    assert "Demand Forecast" in reply


def test_assistant_answers_product_stock(client, create_product):
    create_product(
        name="Amul Butter",
        sku="AMUL-500",
        stock_quantity=7,
        reorder_level=3,
    )

    response = ask(client, "What is the stock of Amul Butter?")
    assert response.status_code == 200
    reply = response.json()["reply"]
    assert "Amul Butter" in reply
    assert "7 units" in reply
    assert "in stock" in reply.lower()


def test_assistant_answers_pending_sales_orders(client, create_product):
    product = create_product(stock_quantity=10)
    order = client.post(
        "/orders/",
        json={
            "customer_name": "Assistant Customer",
            "product_id": product["id"],
            "quantity": 2,
        },
    )
    assert order.status_code == 200
    order_id = order.json()["id"]

    response = ask(client, "Show pending sales orders")
    assert response.status_code == 200
    reply = response.json()["reply"]
    assert f"#{order_id}" in reply
    assert "Assistant Customer" in reply


def test_assistant_answers_how_to_add_product(client):
    response = ask(client, "How do I add a product?")
    assert response.status_code == 200
    reply = response.json()["reply"]
    assert "Products" in reply
    assert "Add Product" in reply
    assert "SKU" in reply


def test_assistant_answers_catalog_counts(client, create_product, create_supplier):
    create_product()
    create_supplier()

    products = ask(client, "How many products are there?").json()["reply"]
    suppliers = ask(client, "How many suppliers?").json()["reply"]

    assert "1 product" in products
    assert "1 supplier" in suppliers


def test_assistant_falls_back_to_local_when_llm_fails(
    client,
    create_product,
    monkeypatch,
):
    monkeypatch.setenv("ASSISTANT_LLM_API_KEY", "test-key-not-real")
    create_product(
        name="Fallback Widget",
        sku="FALLBACK-1",
        stock_quantity=1,
        reorder_level=4,
    )

    def fail_request(*_args, **_kwargs):
        raise requests.RequestException("provider unavailable")

    monkeypatch.setattr("assistant.llm.requests.post", fail_request)

    response = ask(client, "Show low-stock products")
    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "local"
    assert "Fallback Widget" in data["reply"]


def test_assistant_uses_llm_with_project_scope_when_configured(
    client,
    monkeypatch,
):
    monkeypatch.setenv("ASSISTANT_LLM_API_KEY", "test-key-not-real")
    captured = {}

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {
                "choices": [
                    {"message": {"content": "Use the Products page to add an item."}}
                ]
            }

    def fake_post(url, headers=None, json=None, timeout=None):
        captured["url"] = url
        captured["headers"] = headers
        captured["payload"] = json
        captured["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setattr("assistant.llm.requests.post", fake_post)

    response = ask(client, "How do I add a product?")
    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "llm"
    assert data["reply"] == "Use the Products page to add an item."
    assert captured["headers"]["Authorization"] == "Bearer test-key-not-real"
    assert captured["payload"]["model"]
    assert captured["timeout"] == 20

    system_prompts = [
        message["content"]
        for message in captured["payload"]["messages"]
        if message["role"] == "system"
    ]
    assert any("NextGenERP" in prompt for prompt in system_prompts)
    assert any("STRICT SCOPE" in prompt for prompt in system_prompts)
    assert "test-key-not-real" not in data["reply"]
