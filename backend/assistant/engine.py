"""Project-scoped answer engine for the NextGenERP Assistant."""

import re

from .docs import search_docs
from .knowledge import (
    DEFAULT_SUGGESTIONS,
    DOMAIN_TERMS,
    GREETING_TERMS,
    PROJECT_INTRO,
    SCOPE_REFUSAL,
    find_knowledge,
)
from .llm import ask_llm, is_configured
from .snapshot import build_snapshot

MAX_LIST_ITEMS = 10


def _normalize(value: str) -> str:
    return " ".join(str(value or "").lower().split())


def _contains_any(text: str, phrases) -> bool:
    return any(phrase in text for phrase in phrases)


def _money(value) -> str:
    return f"₹{float(value or 0):,.2f}"


def _result(reply: str, mode: str = "local") -> dict:
    return {
        "reply": reply,
        "suggestions": DEFAULT_SUGGESTIONS,
        "mode": mode,
    }


def _is_greeting(text: str) -> bool:
    cleaned = re.sub(r"[^a-z\s]", " ", text).strip()
    words = cleaned.split()
    if not words:
        return False
    if " ".join(words) in GREETING_TERMS:
        return True
    return words[0] in {"hi", "hello", "hey", "namaste"} and len(words) <= 3


def _find_product(text: str, products):
    matches = []
    for product in products:
        for key in (product.get("name"), product.get("sku")):
            key_text = str(key or "").strip().lower()
            if len(key_text) >= 3 and key_text in text:
                matches.append((len(key_text), product))
    return max(matches, key=lambda item: item[0])[1] if matches else None


def _find_supplier(text: str, suppliers):
    matches = []
    for supplier in suppliers:
        key_text = str(supplier.get("name") or "").strip().lower()
        if len(key_text) >= 3 and key_text in text:
            matches.append((len(key_text), supplier))
    return max(matches, key=lambda item: item[0])[1] if matches else None


def _is_project_related(text: str, snapshot: dict) -> bool:
    if any(term in text for term in DOMAIN_TERMS):
        return True
    if _find_product(text, snapshot["products"]):
        return True
    if _find_supplier(text, snapshot["suppliers"]):
        return True
    return False


def _product_status(product: dict) -> str:
    stock = int(product.get("stock") or 0)
    reorder_level = int(product.get("reorder_level") or 0)
    if stock <= 0:
        return "out of stock"
    if stock <= reorder_level:
        return "low stock"
    return "in stock"


def _product_answer(product: dict) -> str:
    return (
        f"{product['name']} ({product['sku']})\n"
        f"- Stock: {product['stock']} units\n"
        f"- Reorder level: {product['reorder_level']}\n"
        f"- Price: {_money(product['price'])}\n"
        f"- Status: {_product_status(product)}\n\n"
        "Open Products to edit it, or Inventory Operations to record a stock "
        "movement."
    )


def _supplier_answer(supplier: dict) -> str:
    rating = supplier.get("performance_rating")
    rating_text = f"{rating:.1f} / 5" if rating is not None else "not rated"
    contact = ", ".join(
        value for value in (supplier.get("email"), supplier.get("phone")) if value
    )
    lines = [
        f"{supplier['name']}",
        f"- Lead time: {supplier['lead_time_days']} days",
        f"- Performance rating: {rating_text}",
    ]
    if contact:
        lines.append(f"- Contact: {contact}")
    lines.append(
        "\nOpen Suppliers to view or update the supplier. Lead time is used in "
        "reorder planning."
    )
    return "\n".join(lines)


def _low_stock_answer(snapshot: dict) -> str:
    low_stock = snapshot["low_stock"]
    out_of_stock = snapshot["out_of_stock"]

    if low_stock:
        lines = [
            f"- {product['name']} ({product['sku']}): {product['stock']} units "
            f"left, reorder level {product['reorder_level']}"
            for product in low_stock[:MAX_LIST_ITEMS]
        ]
        reply = "Products at or below their reorder level:\n" + "\n".join(lines)
        if len(low_stock) > MAX_LIST_ITEMS:
            reply += f"\n...and {len(low_stock) - MAX_LIST_ITEMS} more."
    else:
        reply = "No products are at or below their reorder level right now."

    if out_of_stock:
        names = ", ".join(product["name"] for product in out_of_stock[:6])
        reply += (
            f"\n\nAlso out of stock ({len(out_of_stock)}): {names}"
            + ("..." if len(out_of_stock) > 6 else ".")
        )

    reply += (
        "\n\nOpen Demand Forecast for suggested reorder quantities based on "
        "demand, lead time and safety stock."
    )
    return reply


def _out_of_stock_answer(snapshot: dict) -> str:
    products = snapshot["out_of_stock"]
    if not products:
        return "No products are out of stock right now."
    lines = [
        f"- {product['name']} ({product['sku']}): reorder level "
        f"{product['reorder_level']}"
        for product in products[:MAX_LIST_ITEMS]
    ]
    reply = f"{len(products)} product(s) are out of stock:\n" + "\n".join(lines)
    if len(products) > MAX_LIST_ITEMS:
        reply += f"\n...and {len(products) - MAX_LIST_ITEMS} more."
    return reply + "\n\nUse Inventory Operations for a stock-in movement or create a purchase order."


def _pending_sales_answer(snapshot: dict) -> str:
    orders = [
        order
        for order in snapshot["recent_sales_orders"]
        if order["status"] == "Pending"
    ]
    total = int(snapshot["order_status_counts"].get("Pending", len(orders)))
    if not orders:
        return "There are no pending sales orders right now."

    lines = [
        f"- Order #{order['id']}: {order['customer_name']} — "
        f"{order['product_name'] or 'product'} × {order['quantity']}"
        for order in orders[:MAX_LIST_ITEMS]
    ]
    header = f"{total} pending sales order(s)."
    if total > len(orders):
        header += f" Showing the latest {len(orders)}."
    return header + "\n" + "\n".join(lines) + "\n\nOpen Sales Orders to confirm, ship or cancel an order."


def _pending_purchase_answer(snapshot: dict) -> str:
    open_statuses = {"Pending", "Approved", "Ordered"}
    orders = [
        order
        for order in snapshot["recent_purchase_orders"]
        if order["status"] in open_statuses
    ]
    total = sum(
        int(snapshot["purchase_order_status_counts"].get(status, 0))
        for status in open_statuses
    )
    if not orders:
        return "There are no open purchase orders right now."

    lines = [
        f"- PO #{order['id']}: {order['supplier_name'] or 'supplier'} — "
        f"{order['product_name'] or 'product'} × {order['quantity']} "
        f"({order['status']})"
        for order in orders[:MAX_LIST_ITEMS]
    ]
    header = f"{total} open purchase order(s) (Pending, Approved or Ordered)."
    if total > len(orders):
        header += f" Showing the latest {len(orders)}."
    return header + "\n" + "\n".join(lines) + "\n\nOpen Purchase Orders to approve, order or receive stock."


def _count_answer(text: str, snapshot: dict):
    counts = snapshot["counts"]
    if "product" in text:
        return f"The catalog has {counts['products']} product(s)."
    if "supplier" in text or "vendor" in text:
        return f"There are {counts['suppliers']} supplier(s)."
    if "purchase" in text:
        return f"There are {counts['purchase_orders']} purchase order(s)."
    if "order" in text or "sale" in text:
        return f"There are {counts['sales_orders']} sales order(s)."
    if "categor" in text:
        return f"There are {counts['categories']} categor(y/ies)."
    return None


def _sales_summary_answer(snapshot: dict) -> str:
    counts = snapshot["order_status_counts"]
    statuses = ["Pending", "Confirmed", "Shipped", "Delivered", "Cancelled"]
    lines = [f"- {status}: {int(counts.get(status, 0))}" for status in statuses]
    return (
        f"Sales orders: {snapshot['counts']['sales_orders']} total\n"
        + "\n".join(lines)
        + "\n\nOpen Sales Orders for the full list and status controls."
    )


def _supplier_list_answer(snapshot: dict) -> str:
    suppliers = snapshot["suppliers"]
    if not suppliers:
        return "No suppliers are registered yet. Open Suppliers to add one."
    lines = []
    for supplier in suppliers[:MAX_LIST_ITEMS]:
        rating = supplier.get("performance_rating")
        rating_text = f"{rating:.1f}/5" if rating is not None else "not rated"
        lines.append(
            f"- {supplier['name']}: lead time "
            f"{supplier['lead_time_days']} days, rating {rating_text}"
        )
    reply = f"{len(suppliers)} supplier(s):\n" + "\n".join(lines)
    if len(suppliers) > MAX_LIST_ITEMS:
        reply += f"\n...and {len(suppliers) - MAX_LIST_ITEMS} more."
    return reply


def _order_lookup(text: str, snapshot: dict):
    match = re.search(r"(?:order|#)\s*#?(\d+)", text)
    if not match:
        return None
    order_id = int(match.group(1))
    is_purchase = "purchase" in text or "po " in f"{text} "

    if is_purchase:
        record = next(
            (
                order
                for order in snapshot["recent_purchase_orders"]
                if order["id"] == order_id
            ),
            None,
        )
        if not record:
            return f"I could not find purchase order #{order_id} in the recent records."
        return (
            f"Purchase order #{record['id']}\n"
            f"- Supplier: {record['supplier_name'] or record['supplier_id']}\n"
            f"- Product: {record['product_name'] or record['product_id']}\n"
            f"- Quantity: {record['quantity']}\n"
            f"- Unit price: {_money(record['unit_price'])}\n"
            f"- Total: {_money(record['total_amount'])}\n"
            f"- Status: {record['status']}"
        )

    record = next(
        (
            order
            for order in snapshot["recent_sales_orders"]
            if order["id"] == order_id
        ),
        None,
    )
    if not record:
        return f"I could not find sales order #{order_id} in the recent records."
    return (
        f"Sales order #{record['id']}\n"
        f"- Customer: {record['customer_name']}\n"
        f"- Product: {record['product_name'] or record['product_id']}\n"
        f"- Quantity: {record['quantity']}\n"
        f"- Total: {_money(record['total_amount'])}\n"
        f"- Status: {record['status']}"
    )


def _supplier_for_product(text: str, snapshot: dict):
    product = _find_product(text, snapshot["products"])
    if not product:
        return None
    supplier_names = []
    for order in snapshot["recent_purchase_orders"]:
        if order["product_id"] == product["id"] and order["supplier_name"]:
            if order["supplier_name"] not in supplier_names:
                supplier_names.append(order["supplier_name"])
    if not supplier_names:
        return (
            f"No recent purchase orders link {product['name']} to a supplier. "
            "Open Purchase Orders or Suppliers to check the full record."
        )
    return (
        f"Supplier(s) linked to {product['name']} in recent purchase orders: "
        + ", ".join(supplier_names)
        + "."
    )


def _local_answer(text: str, snapshot: dict, knowledge_entry, doc_match) -> str:
    if knowledge_entry:
        return knowledge_entry["answer"]

    if _contains_any(
        text,
        [
            "low stock", "low on stock", "low-stock", "running low", "reorder",
            "restock", "minimum stock", "stock kam", "kam stock", "need to order",
            "should i order",
        ],
    ):
        return _low_stock_answer(snapshot)

    if _contains_any(text, ["out of stock", "no stock", "zero stock", "khatam"]):
        return _out_of_stock_answer(snapshot)

    if _contains_any(
        text,
        ["pending sales", "pending order", "open sales", "sales pending"],
    ):
        return _pending_sales_answer(snapshot)

    if _contains_any(
        text,
        ["pending purchase", "open purchase", "purchase pending", "awaiting delivery"],
    ):
        return _pending_purchase_answer(snapshot)

    if _contains_any(text, ["how many", "count", "total", "kitne"]):
        count_answer = _count_answer(text, snapshot)
        if count_answer:
            return count_answer

    if _contains_any(
        text,
        ["who supplies", "which supplier", "supplier for", "vendor for"],
    ):
        supplier_answer = _supplier_for_product(text, snapshot)
        if supplier_answer:
            return supplier_answer

    order_answer = _order_lookup(text, snapshot)
    if order_answer:
        return order_answer

    product = _find_product(text, snapshot["products"])
    if product and (
        len(text) <= len(product["name"].lower()) + 25
        or _contains_any(
            text,
            ["stock", "price", "quantity", "sku", "detail", "about", "status"],
        )
    ):
        return _product_answer(product)

    supplier = _find_supplier(text, snapshot["suppliers"])
    if supplier and (
        len(text) <= len(supplier["name"].lower()) + 25
        or _contains_any(text, ["supplier", "vendor", "lead time", "rating", "contact"])
    ):
        return _supplier_answer(supplier)

    if _contains_any(text, ["supplier", "vendor"]):
        return _supplier_list_answer(snapshot)

    if _contains_any(text, ["sales", "orders", "order summary"]):
        return _sales_summary_answer(snapshot)

    if doc_match:
        return (
            f"From {doc_match['source']} — {doc_match['title']}:\n\n"
            f"{doc_match['text'][:900]}"
        )

    return (
        "I could not find that in the current workspace data. I can help with "
        "live stock levels, low-stock items, pending orders, suppliers, product "
        "prices and reorder needs.\n\nTry:\n"
        "- Show low-stock products\n"
        "- What are the pending purchase orders?\n"
        "- What is the stock of a product?\n"
        "- How do I record a stock movement?"
    )


def answer_chat(message: str, db, history=None) -> dict:
    snapshot = build_snapshot(db)
    text = _normalize(message)
    knowledge_entry = find_knowledge(message)
    doc_match = search_docs(message)

    if _is_greeting(text) and not knowledge_entry:
        return _result(
            PROJECT_INTRO
            + "\n\nAsk me about live stock, low-stock items, orders, suppliers "
            "or how to use any page."
        )

    if not (
        knowledge_entry
        or doc_match
        or _is_project_related(text, snapshot)
    ):
        return _result(SCOPE_REFUSAL)

    if is_configured():
        llm_reply = ask_llm(
            message,
            history,
            snapshot,
            knowledge_entry=knowledge_entry,
            doc_match=doc_match,
        )
        if llm_reply:
            return _result(llm_reply, mode="llm")

    return _result(
        _local_answer(text, snapshot, knowledge_entry, doc_match)
    )
