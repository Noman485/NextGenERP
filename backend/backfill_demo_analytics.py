"""Backfill analytics timestamps for the demo dataset.

Existing demo orders and purchase orders were created before the administrator
analytics feature added ``created_at`` columns.  This one-time helper gives the
demo rows a deterministic spread over the last year so the daily/monthly/yearly
charts are useful.  It only touches rows whose timestamps are empty and whose
customer email uses the ``@example.test`` demo domain; real records are left
alone.

Run from the backend directory:

    .\\venv\\Scripts\\python.exe backfill_demo_analytics.py
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from database.connection import engine
from database.migrations import ensure_schema
from models.category import Category  # noqa: F401 - registers the Product relationship target
from models.order import Order
from models.product import Product  # noqa: F401 - registers the Order relationship target
from models.purchase_order import PurchaseOrder
from models.supplier import Supplier  # noqa: F401 - registers the PurchaseOrder relationship target
from models.user import User

DEMO_EMAIL_SUFFIX = "@example.test"


def main() -> int:
    ensure_schema()
    now = datetime.now(timezone.utc)
    orders_updated = 0
    purchases_updated = 0

    with Session(engine) as db:
        demo_user = db.query(User).order_by(User.id).first()
        demo_username = demo_user.username if demo_user is not None else None

        orders = (
            db.query(Order)
            .filter(Order.created_at.is_(None))
            .filter(Order.customer_email.like(f"%{DEMO_EMAIL_SUFFIX}"))
            .order_by(Order.id)
            .all()
        )
        for index, order in enumerate(orders, start=1):
            order.created_at = now - timedelta(
                days=(index * 37) % 365,
                hours=index % 24,
                minutes=(index * 7) % 60,
            )
            if order.user_id is None and demo_user is not None:
                order.user_id = demo_user.id
            orders_updated += 1

        purchases = (
            db.query(PurchaseOrder)
            .filter(PurchaseOrder.created_at.is_(None))
            .order_by(PurchaseOrder.id)
            .all()
        )
        for index, purchase in enumerate(purchases, start=1):
            purchase.created_at = now - timedelta(
                days=(index * 29) % 365,
                hours=(index * 5) % 24,
                minutes=(index * 3) % 60,
            )
            purchases_updated += 1

        db.commit()

    print(f"Backfilled {orders_updated} demo sales orders")
    print(f"Backfilled {purchases_updated} purchase orders")
    if demo_username is not None:
        print(f"Legacy demo orders assigned to user: {demo_username}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
