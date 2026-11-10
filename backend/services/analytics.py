"""Administrator analytics.

All metrics are computed from persisted business records.  Revenue is
"realized" revenue: orders in Confirmed, Shipped or Delivered state.  Pending
orders are reported separately as pipeline value, and cancelled orders are
never counted as revenue.  No statistics are invented.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy.orm import Session

from models.inventory_transaction import InventoryTransaction
from models.order import Order
from models.product import Product
from models.purchase_order import PurchaseOrder
from models.supplier import Supplier
from models.user import User

REALIZED_STATUSES = ("Confirmed", "Shipped", "Delivered")
PIPELINE_STATUSES = ("Pending", "Confirmed", "Shipped")
PURCHASE_PENDING_STATUSES = ("Pending", "Approved", "Ordered")


def _decimal(value) -> Decimal:
    if value is None:
        return Decimal("0")
    return Decimal(str(value))


def money(value) -> float:
    return float(_decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def _as_utc(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _iso(value: datetime | None) -> str | None:
    normalized = _as_utc(value)
    return normalized.isoformat() if normalized else None


def _order_summary(orders: list[Order]) -> dict:
    statuses = Counter((order.status or "Unknown") for order in orders)
    realized = [order for order in orders if order.status in REALIZED_STATUSES]
    pending = [order for order in orders if order.status == "Pending"]
    cancelled = [order for order in orders if order.status == "Cancelled"]

    realized_revenue = sum((_decimal(order.total_amount) for order in realized), Decimal("0"))
    pending_revenue = sum((_decimal(order.total_amount) for order in pending), Decimal("0"))
    cancelled_value = sum((_decimal(order.total_amount) for order in cancelled), Decimal("0"))
    average_order_value = (
        realized_revenue / len(realized) if realized else Decimal("0")
    )

    return {
        "total_orders": len(orders),
        "pending_orders": statuses.get("Pending", 0),
        "confirmed_orders": statuses.get("Confirmed", 0),
        "shipped_orders": statuses.get("Shipped", 0),
        "completed_orders": statuses.get("Delivered", 0),
        "cancelled_orders": statuses.get("Cancelled", 0),
        "realized_orders": len(realized),
        "realized_revenue": money(realized_revenue),
        "pipeline_revenue": money(pending_revenue),
        "cancelled_value": money(cancelled_value),
        "average_order_value": money(average_order_value),
    }


def _range_totals(orders: list[Order]) -> dict:
    summary = _order_summary(orders)
    return {
        "orders": summary["total_orders"],
        "realized_orders": summary["realized_orders"],
        "completed_orders": summary["completed_orders"],
        "cancelled_orders": summary["cancelled_orders"],
        "revenue": summary["realized_revenue"],
        "average_order_value": summary["average_order_value"],
    }


def overview(db: Session) -> dict:
    orders = db.query(Order).all()
    products = db.query(Product).all()
    suppliers = db.query(Supplier).all()
    purchase_orders = db.query(PurchaseOrder).all()
    users = db.query(User).all()

    summary = _order_summary(orders)
    stock_units = sum(max(0, int(product.stock_quantity or 0)) for product in products)
    inventory_value = sum(
        (_decimal(product.stock_quantity or 0) * _decimal(product.price or 0))
        for product in products
    )
    low_stock = [
        product
        for product in products
        if 0 < int(product.stock_quantity or 0) <= int(product.reorder_level or 0)
    ]
    out_of_stock = [
        product for product in products if int(product.stock_quantity or 0) <= 0
    ]

    received_purchases = [
        purchase for purchase in purchase_orders if purchase.status == "Received"
    ]
    pending_purchases = [
        purchase
        for purchase in purchase_orders
        if purchase.status in PURCHASE_PENDING_STATUSES
    ]
    purchase_expenditure = sum(
        (_decimal(purchase.total_amount) for purchase in received_purchases),
        Decimal("0"),
    )
    pending_purchase_value = sum(
        (_decimal(purchase.total_amount) for purchase in pending_purchases),
        Decimal("0"),
    )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "revenue_definition": (
            "Realized revenue includes Confirmed, Shipped and Delivered sales "
            "orders. Pending orders are shown separately. Cancelled orders are excluded."
        ),
        **summary,
        "total_sales": summary["realized_orders"],
        "total_sales_revenue": summary["realized_revenue"],
        "total_users": len(users),
        "active_users": sum(1 for user in users if user.is_active),
        "total_products": len(products),
        "total_suppliers": len(suppliers),
        "total_inventory_units": stock_units,
        "inventory_value_at_selling_price": money(inventory_value),
        "inventory_value_note": (
            "Inventory is valued at the product selling price because purchase cost "
            "is not stored on the product record."
        ),
        "low_stock_products": len(low_stock),
        "out_of_stock_products": len(out_of_stock),
        "purchase_orders": len(purchase_orders),
        "received_purchase_orders": len(received_purchases),
        "pending_purchase_orders": sum(
            1 for purchase in purchase_orders if purchase.status == "Pending"
        ),
        "cancelled_purchase_orders": sum(
            1 for purchase in purchase_orders if purchase.status == "Cancelled"
        ),
        "purchase_expenditure": money(purchase_expenditure),
        "pending_purchase_value": money(pending_purchase_value),
        "purchase_expenditure_note": (
            "Purchase expenditure includes Received purchase orders only."
        ),
    }


def daily_sales(db: Session, days: int = 30, today: date | None = None) -> dict:
    orders = db.query(Order).all()
    end_day = today or datetime.now(timezone.utc).date()
    start_day = end_day - timedelta(days=days - 1)
    buckets: dict[date, list[Order]] = {
        start_day + timedelta(days=offset): [] for offset in range(days)
    }
    undated = 0

    for order in orders:
        created = _as_utc(order.created_at)
        if created is None:
            undated += 1
            continue
        order_day = created.date()
        if start_day <= order_day <= end_day:
            buckets[order_day].append(order)

    series = []
    for day in sorted(buckets):
        summary = _order_summary(buckets[day])
        series.append(
            {
                "date": day.isoformat(),
                "revenue": summary["realized_revenue"],
                "orders": summary["total_orders"],
                "completed_orders": summary["completed_orders"],
                "cancelled_orders": summary["cancelled_orders"],
                "average_order_value": summary["average_order_value"],
            }
        )

    range_orders = [order for bucket in buckets.values() for order in bucket]
    return {
        "start": start_day.isoformat(),
        "end": end_day.isoformat(),
        "days": days,
        "undated_orders": undated,
        "totals": _range_totals(range_orders),
        "series": series,
    }


def monthly_sales(db: Session, year: int) -> dict:
    orders = db.query(Order).all()
    buckets: dict[int, list[Order]] = {month: [] for month in range(1, 13)}
    undated = 0
    outside_year = 0

    for order in orders:
        created = _as_utc(order.created_at)
        if created is None:
            undated += 1
            continue
        if created.year == year:
            buckets[created.month].append(order)
        else:
            outside_year += 1

    series = []
    previous_revenue: Decimal | None = None
    for month in range(1, 13):
        summary = _order_summary(buckets[month])
        revenue = _decimal(summary["realized_revenue"])
        if previous_revenue is None:
            growth = None
        elif previous_revenue == 0:
            growth = None if revenue == 0 else 100.0
        else:
            growth = float(
                ((revenue - previous_revenue) / previous_revenue * Decimal("100")).quantize(
                    Decimal("0.01"), rounding=ROUND_HALF_UP
                )
            )
        series.append(
            {
                "month": month,
                "label": date(year, month, 1).strftime("%B"),
                "revenue": summary["realized_revenue"],
                "orders": summary["total_orders"],
                "completed_orders": summary["completed_orders"],
                "cancelled_orders": summary["cancelled_orders"],
                "average_order_value": summary["average_order_value"],
                "previous_month_growth_percent": growth,
            }
        )
        previous_revenue = revenue

    all_year_orders = [order for bucket in buckets.values() for order in bucket]
    return {
        "year": year,
        "undated_orders": undated,
        "orders_outside_year": outside_year,
        "totals": _range_totals(all_year_orders),
        "series": series,
    }


def yearly_sales(db: Session, years: int = 5, current_year: int | None = None) -> dict:
    orders = db.query(Order).all()
    end_year = current_year or datetime.now(timezone.utc).year
    start_year = end_year - years + 1
    buckets: dict[int, list[Order]] = {year: [] for year in range(start_year, end_year + 1)}
    undated = 0

    for order in orders:
        created = _as_utc(order.created_at)
        if created is None:
            undated += 1
            continue
        if start_year <= created.year <= end_year:
            buckets[created.year].append(order)

    series = []
    previous_revenue: Decimal | None = None
    for year in sorted(buckets):
        summary = _order_summary(buckets[year])
        revenue = _decimal(summary["realized_revenue"])
        if previous_revenue is None:
            growth = None
        elif previous_revenue == 0:
            growth = None if revenue == 0 else 100.0
        else:
            growth = float(
                ((revenue - previous_revenue) / previous_revenue * Decimal("100")).quantize(
                    Decimal("0.01"), rounding=ROUND_HALF_UP
                )
            )
        series.append(
            {
                "year": year,
                "revenue": summary["realized_revenue"],
                "orders": summary["total_orders"],
                "completed_orders": summary["completed_orders"],
                "cancelled_orders": summary["cancelled_orders"],
                "average_order_value": summary["average_order_value"],
                "year_over_year_growth_percent": growth,
            }
        )
        previous_revenue = revenue

    range_orders = [order for bucket in buckets.values() for order in bucket]
    return {
        "start_year": start_year,
        "end_year": end_year,
        "undated_orders": undated,
        "totals": _range_totals(range_orders),
        "series": series,
    }


def _user_rows(db: Session) -> list[dict]:
    users = db.query(User).all()
    orders = db.query(Order).all()
    by_user: dict[int | None, list[Order]] = defaultdict(list)
    for order in orders:
        by_user[order.user_id].append(order)

    rows = []
    for user in users:
        summary = _order_summary(by_user.get(user.id, []))
        rows.append(
            {
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role or "USER",
                "is_active": bool(user.is_active),
                "created_at": _iso(user.created_at),
                "last_login_at": _iso(user.last_login_at),
                "orders": summary["total_orders"],
                "realized_orders": summary["realized_orders"],
                "completed_orders": summary["completed_orders"],
                "cancelled_orders": summary["cancelled_orders"],
                "revenue": summary["realized_revenue"],
                "average_order_value": summary["average_order_value"],
            }
        )

    unassigned = by_user.get(None, [])
    if unassigned:
        summary = _order_summary(unassigned)
        rows.append(
            {
                "user_id": None,
                "username": "Unassigned (legacy orders)",
                "email": None,
                "role": None,
                "is_active": None,
                "created_at": None,
                "last_login_at": None,
                "orders": summary["total_orders"],
                "realized_orders": summary["realized_orders"],
                "completed_orders": summary["completed_orders"],
                "cancelled_orders": summary["cancelled_orders"],
                "revenue": summary["realized_revenue"],
                "average_order_value": summary["average_order_value"],
            }
        )
    return rows


def user_sales(
    db: Session,
    query: str | None = None,
    sort: str = "revenue",
    direction: str = "desc",
    limit: int = 100,
    offset: int = 0,
) -> dict:
    rows = _user_rows(db)
    if query:
        needle = query.strip().lower()
        rows = [
            row
            for row in rows
            if needle in (row["username"] or "").lower()
            or needle in (row["email"] or "").lower()
        ]

    sort_key = {
        "revenue": "revenue",
        "orders": "orders",
        "username": "username",
        "created_at": "created_at",
    }.get(sort, "revenue")
    rows.sort(
        key=lambda row: (row.get(sort_key) is None, row.get(sort_key)),
        reverse=direction != "asc",
    )
    total = len(rows)
    return {
        "total": total,
        "items": rows[offset : offset + limit],
        "sort": sort_key,
        "direction": direction,
    }


def user_sales_summary(db: Session, user_id: int) -> dict:
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    summary = _order_summary(orders)
    return {
        "orders": summary["total_orders"],
        "realized_orders": summary["realized_orders"],
        "completed_orders": summary["completed_orders"],
        "cancelled_orders": summary["cancelled_orders"],
        "revenue": summary["realized_revenue"],
        "average_order_value": summary["average_order_value"],
    }


def product_sales(
    db: Session,
    query: str | None = None,
    sort: str = "revenue",
    direction: str = "desc",
    limit: int = 100,
    offset: int = 0,
    today: date | None = None,
) -> dict:
    products = db.query(Product).all()
    orders = db.query(Order).all()
    end_day = today or datetime.now(timezone.utc).date()
    cutoff = datetime.combine(end_day - timedelta(days=29), datetime.min.time(), tzinfo=timezone.utc)
    by_product: dict[int, list[Order]] = defaultdict(list)
    for order in orders:
        by_product[order.product_id].append(order)

    rows = []
    for product in products:
        product_orders = by_product.get(product.id, [])
        non_cancelled = [order for order in product_orders if order.status != "Cancelled"]
        realized = [order for order in product_orders if order.status in REALIZED_STATUSES]
        recent_realized = [
            order
            for order in realized
            if _as_utc(order.created_at) is not None and _as_utc(order.created_at) >= cutoff
        ]
        summary = _order_summary(product_orders)
        stock = int(product.stock_quantity or 0)
        reorder = int(product.reorder_level or 0)
        if stock <= 0:
            stock_status = "Out of stock"
        elif stock <= reorder:
            stock_status = "Low stock"
        else:
            stock_status = "In stock"

        rows.append(
            {
                "product_id": product.id,
                "name": product.name,
                "sku": product.sku,
                "category_id": product.category_id,
                "price": money(product.price),
                "stock_quantity": stock,
                "reorder_level": reorder,
                "stock_status": stock_status,
                "orders": len(product_orders),
                "units_sold": sum(int(order.quantity or 0) for order in non_cancelled),
                "realized_units": sum(int(order.quantity or 0) for order in realized),
                "units_sold_last_30_days": sum(
                    int(order.quantity or 0) for order in recent_realized
                ),
                "cancelled_orders": sum(
                    1 for order in product_orders if order.status == "Cancelled"
                ),
                "revenue": summary["realized_revenue"],
                "average_order_value": summary["average_order_value"],
                "slow_moving_last_30_days": len(recent_realized) == 0,
            }
        )

    if query:
        needle = query.strip().lower()
        rows = [
            row
            for row in rows
            if needle in row["name"].lower() or needle in (row["sku"] or "").lower()
        ]

    sort_key = {
        "revenue": "revenue",
        "units": "units_sold",
        "name": "name",
        "stock": "stock_quantity",
    }.get(sort, "revenue")
    rows.sort(
        key=lambda row: (row.get(sort_key) is None, row.get(sort_key)),
        reverse=direction != "asc",
    )
    best_sellers = sorted(rows, key=lambda row: row["revenue"], reverse=True)[:10]
    slow_moving = sorted(
        [row for row in rows if row["slow_moving_last_30_days"]],
        key=lambda row: (row["stock_quantity"], row["name"]),
        reverse=True,
    )[:10]
    return {
        "total": len(rows),
        "items": rows[offset : offset + limit],
        "best_sellers": best_sellers,
        "slow_moving": slow_moving,
        "slow_moving_definition": (
            "No realized sales (Confirmed, Shipped or Delivered) in the last 30 days."
        ),
        "sort": sort_key,
        "direction": direction,
    }


def supplier_purchases(
    db: Session,
    query: str | None = None,
    sort: str = "purchase_expenditure",
    direction: str = "desc",
    limit: int = 100,
    offset: int = 0,
) -> dict:
    suppliers = db.query(Supplier).all()
    purchase_orders = db.query(PurchaseOrder).all()
    by_supplier: dict[int, list[PurchaseOrder]] = defaultdict(list)
    for purchase in purchase_orders:
        by_supplier[purchase.supplier_id].append(purchase)

    rows = []
    for supplier in suppliers:
        purchases = by_supplier.get(supplier.id, [])
        received = [purchase for purchase in purchases if purchase.status == "Received"]
        pending = [
            purchase
            for purchase in purchases
            if purchase.status in PURCHASE_PENDING_STATUSES
        ]
        expenditure = sum(
            (_decimal(purchase.total_amount) for purchase in received), Decimal("0")
        )
        pending_value = sum(
            (_decimal(purchase.total_amount) for purchase in pending), Decimal("0")
        )
        last_purchase = max(
            (
                _as_utc(purchase.created_at)
                for purchase in purchases
                if _as_utc(purchase.created_at) is not None
            ),
            default=None,
        )
        rows.append(
            {
                "supplier_id": supplier.id,
                "name": supplier.name,
                "email": supplier.email,
                "phone": supplier.phone,
                "lead_time_days": supplier.lead_time_days,
                "performance_rating": supplier.performance_rating,
                "purchase_orders": len(purchases),
                "pending_purchases": sum(
                    1 for purchase in purchases if purchase.status == "Pending"
                ),
                "approved_purchases": sum(
                    1 for purchase in purchases if purchase.status == "Approved"
                ),
                "ordered_purchases": sum(
                    1 for purchase in purchases if purchase.status == "Ordered"
                ),
                "received_purchases": len(received),
                "cancelled_purchases": sum(
                    1 for purchase in purchases if purchase.status == "Cancelled"
                ),
                "purchase_expenditure": money(expenditure),
                "pending_value": money(pending_value),
                "average_received_value": money(
                    expenditure / len(received) if received else Decimal("0")
                ),
                "last_purchase_at": _iso(last_purchase),
            }
        )

    if query:
        needle = query.strip().lower()
        rows = [
            row
            for row in rows
            if needle in row["name"].lower() or needle in (row["email"] or "").lower()
        ]

    sort_key = {
        "purchase_expenditure": "purchase_expenditure",
        "orders": "purchase_orders",
        "name": "name",
        "received": "received_purchases",
    }.get(sort, "purchase_expenditure")
    rows.sort(
        key=lambda row: (row.get(sort_key) is None, row.get(sort_key)),
        reverse=direction != "asc",
    )
    return {
        "total": len(rows),
        "items": rows[offset : offset + limit],
        "sort": sort_key,
        "direction": direction,
    }


def inventory_analytics(db: Session, today: date | None = None) -> dict:
    products = db.query(Product).all()
    transactions = db.query(InventoryTransaction).all()
    end_day = today or datetime.now(timezone.utc).date()
    cutoff = datetime.combine(end_day - timedelta(days=29), datetime.min.time(), tzinfo=timezone.utc)

    low_stock = []
    out_of_stock = []
    total_units = 0
    inventory_value = Decimal("0")
    product_map = {product.id: product for product in products}

    for product in products:
        stock = int(product.stock_quantity or 0)
        reorder = int(product.reorder_level or 0)
        total_units += max(0, stock)
        inventory_value += _decimal(stock) * _decimal(product.price or 0)
        item = {
            "product_id": product.id,
            "name": product.name,
            "sku": product.sku,
            "stock_quantity": stock,
            "reorder_level": reorder,
            "price": money(product.price),
        }
        if stock <= 0:
            out_of_stock.append(item)
        elif stock <= reorder:
            low_stock.append(item)

    recent = [
        transaction
        for transaction in transactions
        if _as_utc(transaction.created_at) is not None
        and _as_utc(transaction.created_at) >= cutoff
    ]
    stock_in_units = sum(
        int(transaction.quantity or 0)
        for transaction in recent
        if transaction.transaction_type == "Stock In"
    )
    stock_out_units = sum(
        int(transaction.quantity or 0)
        for transaction in recent
        if transaction.transaction_type == "Stock Out"
    )

    recent_rows = []
    for transaction in sorted(
        transactions,
        key=lambda item: _as_utc(item.created_at) or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )[:20]:
        product = product_map.get(transaction.product_id)
        recent_rows.append(
            {
                "id": transaction.id,
                "product_id": transaction.product_id,
                "product_name": product.name if product else None,
                "transaction_type": transaction.transaction_type,
                "quantity": transaction.quantity,
                "previous_stock": transaction.previous_stock,
                "new_stock": transaction.new_stock,
                "reason": transaction.reason,
                "created_at": _iso(transaction.created_at),
            }
        )

    return {
        "total_products": len(products),
        "total_units": total_units,
        "inventory_value_at_selling_price": money(inventory_value),
        "inventory_value_note": (
            "Valued at the product selling price because purchase cost is not stored "
            "on the product record."
        ),
        "low_stock_count": len(low_stock),
        "out_of_stock_count": len(out_of_stock),
        "low_stock_products": sorted(low_stock, key=lambda item: item["stock_quantity"]),
        "out_of_stock_products": sorted(out_of_stock, key=lambda item: item["name"]),
        "stock_movements_last_30_days": {
            "stock_in_units": stock_in_units,
            "stock_out_units": stock_out_units,
            "net_units": stock_in_units - stock_out_units,
            "transactions": len(recent),
        },
        "recent_movements": recent_rows,
    }
