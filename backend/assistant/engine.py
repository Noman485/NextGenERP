"""Project-scoped answer engine for the NextGenERP Assistant."""

import re

from .docs import search_docs
from .knowledge import find_knowledge
from .llm import ask_llm, is_configured
from .localization import (
    domain_terms,
    entity_terms,
    fallback_text,
    greeting_first_words,
    greeting_terms,
    intro_text,
    knowledge_answer,
    normalize_language,
    product_status_label,
    purchase_terms,
    refusal_text,
    status_label,
    suggestions_for,
    terms_for,
    text,
)
from .snapshot import build_snapshot

MAX_LIST_ITEMS = 10


def _normalize(value: str) -> str:
    return " ".join(str(value or "").lower().split())


def _contains_any(value: str, phrases) -> bool:
    return any(phrase in value for phrase in phrases)


def _money(value) -> str:
    return f"₹{float(value or 0):,.2f}"


def _result(reply: str, language: str = "en", mode: str = "local") -> dict:
    return {
        "reply": reply,
        "suggestions": suggestions_for(language),
        "mode": mode,
        "language": normalize_language(language),
    }


def _is_greeting(value: str, language: str) -> bool:
    # Keep Devanagari and Bengali combining marks, which ``\w`` alone drops.
    cleaned = re.sub(
        r"[^\w\s\u0900-\u097f\u0980-\u09ff]",
        " ",
        value,
        flags=re.UNICODE,
    ).strip()
    words = cleaned.split()
    if not words:
        return False
    if " ".join(words) in greeting_terms(language):
        return True
    return words[0] in greeting_first_words(language) and len(words) <= 3


def _find_product(value: str, products):
    matches = []
    for product in products:
        for key in (product.get("name"), product.get("sku")):
            key_text = str(key or "").strip().lower()
            if len(key_text) >= 3 and key_text in value:
                matches.append((len(key_text), product))
    return max(matches, key=lambda item: item[0])[1] if matches else None


def _find_supplier(value: str, suppliers):
    matches = []
    for supplier in suppliers:
        key_text = str(supplier.get("name") or "").strip().lower()
        if len(key_text) >= 3 and key_text in value:
            matches.append((len(key_text), supplier))
    return max(matches, key=lambda item: item[0])[1] if matches else None


def _is_project_related(value: str, snapshot: dict, language: str) -> bool:
    if any(term in value for term in domain_terms(language)):
        return True
    if _find_product(value, snapshot["products"]):
        return True
    if _find_supplier(value, snapshot["suppliers"]):
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


def _product_answer(product: dict, language: str) -> str:
    return text(
        language,
        "product_detail",
        name=product["name"],
        sku=product["sku"],
        stock=product["stock"],
        reorder_level=product["reorder_level"],
        price=_money(product["price"]),
        status=product_status_label(_product_status(product), language),
    )


def _supplier_answer(supplier: dict, language: str) -> str:
    rating = supplier.get("performance_rating")
    rating_text = (
        f"{rating:.1f} / 5"
        if rating is not None
        else text(language, "not_rated")
    )
    contact = ", ".join(
        value for value in (supplier.get("email"), supplier.get("phone")) if value
    )
    lines = [
        text(
            language,
            "supplier_detail_head",
            name=supplier["name"],
            lead_time=supplier["lead_time_days"],
            rating=rating_text,
        )
    ]
    if contact:
        lines.append(text(language, "supplier_contact", contact=contact))
    lines.append("\n" + text(language, "supplier_hint"))
    return "\n".join(lines)


def _low_stock_answer(snapshot: dict, language: str) -> str:
    low_stock = snapshot["low_stock"]
    out_of_stock = snapshot["out_of_stock"]

    if low_stock:
        lines = [
            text(
                language,
                "low_stock_line",
                name=product["name"],
                sku=product["sku"],
                stock=product["stock"],
                reorder_level=product["reorder_level"],
            )
            for product in low_stock[:MAX_LIST_ITEMS]
        ]
        reply = text(language, "low_stock_header") + "\n" + "\n".join(lines)
        if len(low_stock) > MAX_LIST_ITEMS:
            reply += "\n" + text(
                language, "more_line", count=len(low_stock) - MAX_LIST_ITEMS
            )
    else:
        reply = text(language, "low_stock_none")

    if out_of_stock:
        names = ", ".join(
            product["name"] for product in out_of_stock[:6]
        ) + ("..." if len(out_of_stock) > 6 else ".")
        reply += "\n\n" + text(
            language,
            "out_of_stock_extra",
            count=len(out_of_stock),
            names=names,
        )

    reply += "\n\n" + text(language, "forecast_hint")
    return reply


def _out_of_stock_answer(snapshot: dict, language: str) -> str:
    products = snapshot["out_of_stock"]
    if not products:
        return text(language, "out_of_stock_none")
    lines = [
        text(
            language,
            "out_of_stock_line",
            name=product["name"],
            sku=product["sku"],
            reorder_level=product["reorder_level"],
        )
        for product in products[:MAX_LIST_ITEMS]
    ]
    reply = text(language, "out_of_stock_header", count=len(products))
    reply += "\n" + "\n".join(lines)
    if len(products) > MAX_LIST_ITEMS:
        reply += "\n" + text(
            language, "more_line", count=len(products) - MAX_LIST_ITEMS
        )
    return reply + "\n\n" + text(language, "out_of_stock_hint")


def _pending_sales_answer(snapshot: dict, language: str) -> str:
    orders = [
        order
        for order in snapshot["recent_sales_orders"]
        if order["status"] == "Pending"
    ]
    total = int(snapshot["order_status_counts"].get("Pending", len(orders)))
    if not orders:
        return text(language, "no_pending_sales")

    lines = [
        text(
            language,
            "pending_sales_line",
            id=order["id"],
            customer=order["customer_name"],
            product=order["product_name"]
            or text(language, "generic_product"),
            quantity=order["quantity"],
        )
        for order in orders[:MAX_LIST_ITEMS]
    ]
    header = text(language, "pending_sales_header", count=total)
    if total > len(orders):
        header += text(language, "showing_latest", count=len(orders))
    return (
        header
        + "\n"
        + "\n".join(lines)
        + "\n\n"
        + text(language, "sales_hint")
    )


def _pending_purchase_answer(snapshot: dict, language: str) -> str:
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
        return text(language, "no_open_purchases")

    lines = [
        text(
            language,
            "open_purchases_line",
            id=order["id"],
            supplier=order["supplier_name"]
            or text(language, "generic_supplier"),
            product=order["product_name"]
            or text(language, "generic_product"),
            quantity=order["quantity"],
            status=status_label(order["status"], language),
        )
        for order in orders[:MAX_LIST_ITEMS]
    ]
    header = text(language, "open_purchases_header", count=total)
    if total > len(orders):
        header += text(language, "showing_latest", count=len(orders))
    return (
        header
        + "\n"
        + "\n".join(lines)
        + "\n\n"
        + text(language, "purchases_hint")
    )


def _count_answer(value: str, snapshot: dict, language: str):
    counts = snapshot["counts"]
    if _contains_any(value, entity_terms("product", language)):
        return text(language, "count_products", count=counts["products"])
    if _contains_any(value, entity_terms("supplier", language)):
        return text(language, "count_suppliers", count=counts["suppliers"])
    if _contains_any(value, entity_terms("purchase", language)):
        return text(
            language,
            "count_purchase_orders",
            count=counts["purchase_orders"],
        )
    if _contains_any(value, entity_terms("order", language)):
        return text(language, "count_sales_orders", count=counts["sales_orders"])
    if _contains_any(value, entity_terms("category", language)):
        return text(language, "count_categories", count=counts["categories"])
    return None


def _sales_summary_answer(snapshot: dict, language: str) -> str:
    counts = snapshot["order_status_counts"]
    statuses = ["Pending", "Confirmed", "Shipped", "Delivered", "Cancelled"]
    lines = [
        text(
            language,
            "sales_summary_line",
            status=status_label(status, language),
            count=int(counts.get(status, 0)),
        )
        for status in statuses
    ]
    return (
        text(
            language,
            "sales_summary_header",
            count=snapshot["counts"]["sales_orders"],
        )
        + "\n"
        + "\n".join(lines)
        + "\n\n"
        + text(language, "sales_summary_hint")
    )


def _supplier_list_answer(snapshot: dict, language: str) -> str:
    suppliers = snapshot["suppliers"]
    if not suppliers:
        return text(language, "no_suppliers")
    lines = []
    for supplier in suppliers[:MAX_LIST_ITEMS]:
        rating = supplier.get("performance_rating")
        rating_text = (
            f"{rating:.1f}/5"
            if rating is not None
            else text(language, "not_rated")
        )
        lines.append(
            text(
                language,
                "supplier_list_line",
                name=supplier["name"],
                lead_time=supplier["lead_time_days"],
                rating=rating_text,
            )
        )
    reply = (
        text(language, "supplier_list_header", count=len(suppliers))
        + "\n"
        + "\n".join(lines)
    )
    if len(suppliers) > MAX_LIST_ITEMS:
        reply += "\n" + text(
            language, "more_line", count=len(suppliers) - MAX_LIST_ITEMS
        )
    return reply


def _order_lookup(value: str, snapshot: dict, language: str):
    match = re.search(r"(?:order|#|ऑर्डर|অর্ডার)\s*#?(\d+)", value)
    if not match:
        return None
    order_id = int(match.group(1))
    is_purchase = _contains_any(value, purchase_terms(language))

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
            return text(language, "not_found_purchase", id=order_id)
        return "\n".join(
            [
                text(language, "purchase_order_title", id=record["id"]),
                text(
                    language,
                    "label_supplier",
                    value=record["supplier_name"] or record["supplier_id"],
                ),
                text(
                    language,
                    "label_product",
                    value=record["product_name"] or record["product_id"],
                ),
                text(language, "label_quantity", value=record["quantity"]),
                text(
                    language,
                    "label_unit_price",
                    value=_money(record["unit_price"]),
                ),
                text(
                    language,
                    "label_total",
                    value=_money(record["total_amount"]),
                ),
                text(
                    language,
                    "label_status",
                    value=status_label(record["status"], language),
                ),
            ]
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
        return text(language, "not_found_sales", id=order_id)
    return "\n".join(
        [
            text(language, "sales_order_title", id=record["id"]),
            text(language, "label_customer", value=record["customer_name"]),
            text(
                language,
                "label_product",
                value=record["product_name"] or record["product_id"],
            ),
            text(language, "label_quantity", value=record["quantity"]),
            text(
                language,
                "label_total",
                value=_money(record["total_amount"]),
            ),
            text(
                language,
                "label_status",
                value=status_label(record["status"], language),
            ),
        ]
    )


def _supplier_for_product(value: str, snapshot: dict, language: str):
    product = _find_product(value, snapshot["products"])
    if not product:
        return None
    supplier_names = []
    for order in snapshot["recent_purchase_orders"]:
        if order["product_id"] == product["id"] and order["supplier_name"]:
            if order["supplier_name"] not in supplier_names:
                supplier_names.append(order["supplier_name"])
    if not supplier_names:
        return text(language, "supplier_for_none", product=product["name"])
    return text(
        language,
        "supplier_for_header",
        product=product["name"],
        suppliers=", ".join(supplier_names),
    )


def _local_answer(
    value: str,
    snapshot: dict,
    knowledge_entry,
    doc_match,
    language: str,
) -> str:
    if knowledge_entry:
        return knowledge_answer(knowledge_entry, language)

    if _contains_any(value, terms_for("low_stock", language)):
        return _low_stock_answer(snapshot, language)

    if _contains_any(value, terms_for("out_of_stock", language)):
        return _out_of_stock_answer(snapshot, language)

    if _contains_any(value, terms_for("pending_sales", language)):
        return _pending_sales_answer(snapshot, language)

    if _contains_any(value, terms_for("pending_purchase", language)):
        return _pending_purchase_answer(snapshot, language)

    if _contains_any(value, terms_for("count", language)):
        count_answer = _count_answer(value, snapshot, language)
        if count_answer:
            return count_answer

    if _contains_any(value, terms_for("supplier_for", language)):
        supplier_answer = _supplier_for_product(value, snapshot, language)
        if supplier_answer:
            return supplier_answer

    order_answer = _order_lookup(value, snapshot, language)
    if order_answer:
        return order_answer

    product = _find_product(value, snapshot["products"])
    if product and (
        len(value) <= len(product["name"].lower()) + 25
        or _contains_any(value, terms_for("product_detail", language))
    ):
        return _product_answer(product, language)

    supplier = _find_supplier(value, snapshot["suppliers"])
    if supplier and (
        len(value) <= len(supplier["name"].lower()) + 25
        or _contains_any(value, terms_for("supplier_detail", language))
    ):
        return _supplier_answer(supplier, language)

    if _contains_any(value, terms_for("supplier_list", language)):
        return _supplier_list_answer(snapshot, language)

    if _contains_any(value, terms_for("sales_summary", language)):
        return _sales_summary_answer(snapshot, language)

    if doc_match:
        return (
            text(
                language,
                "doc_from",
                source=doc_match["source"],
                title=doc_match["title"],
            )
            + "\n\n"
            + doc_match["text"][:900]
        )

    return fallback_text(language)


def answer_chat(message: str, db, history=None, language: str = "en") -> dict:
    language = normalize_language(language)
    snapshot = build_snapshot(db)
    value = _normalize(message)
    knowledge_entry = find_knowledge(message, language)
    doc_match = search_docs(message)

    if _is_greeting(value, language) and not knowledge_entry:
        return _result(intro_text(language), language)

    if not (
        knowledge_entry
        or doc_match
        or _is_project_related(value, snapshot, language)
    ):
        return _result(refusal_text(language), language)

    if is_configured():
        llm_reply = ask_llm(
            message,
            history,
            snapshot,
            knowledge_entry=knowledge_entry,
            doc_match=doc_match,
            language=language,
        )
        if llm_reply:
            return _result(llm_reply, language, mode="llm")

    return _result(
        _local_answer(value, snapshot, knowledge_entry, doc_match, language),
        language,
    )
