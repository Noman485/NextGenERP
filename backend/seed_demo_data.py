"""Populate the local NextGenERP database with demo data.

The script brings every business module to at least 100 rows while preserving
existing records. It is idempotent: rerunning it tops up any module that is
still short instead of duplicating the previous seed.

Stock movements go through the same ``change_stock`` service used by the API, so
sales orders deduct stock, cancellations restore it, and received purchase
orders add it exactly once.

Run from the backend directory:

    .\\venv\\Scripts\\python.exe seed_demo_data.py
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from database.connection import engine
from models.category import Category
from models.inventory_transaction import InventoryTransaction
from models.order import Order
from models.product import Product
from models.purchase_order import PurchaseOrder
from models.supplier import Supplier
from models.user import User
from services.inventory import change_stock

TARGET = 100

DEPARTMENTS = [
    "Dairy",
    "Bakery",
    "Beverages",
    "Snacks",
    "Staples",
    "Frozen",
    "Household",
    "Personal Care",
    "Confectionery",
    "Ready to Eat",
]

SUBCATEGORIES = [
    "Milk & Butter",
    "Bread & Buns",
    "Juices & Soda",
    "Chips & Namkeen",
    "Rice & Flour",
    "Frozen Meals",
    "Cleaning",
    "Hygiene",
    "Chocolate",
    "Instant Food",
]

PRODUCT_ITEMS = [
    "Milk",
    "Butter",
    "Cheese",
    "Yogurt",
    "Bread",
    "Buns",
    "Orange Juice",
    "Cola",
    "Potato Chips",
    "Namkeen",
    "Basmati Rice",
    "Wheat Flour",
    "Frozen Peas",
    "Ice Cream",
    "Dish Soap",
    "Shampoo",
    "Chocolate Bar",
    "Instant Noodles",
    "Tea",
    "Coffee",
]

PRODUCT_VARIANTS = ["Classic", "Premium", "Family Pack", "Value Pack", "Organic"]

SALES_STATUSES = (
    ["Pending"] * 30
    + ["Confirmed"] * 20
    + ["Shipped"] * 15
    + ["Delivered"] * 20
    + ["Cancelled"] * 15
)

PURCHASE_STATUSES = (
    ["Pending"] * 30
    + ["Approved"] * 20
    + ["Ordered"] * 15
    + ["Received"] * 25
    + ["Cancelled"] * 10
)

CUSTOMER_FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh",
    "Ayaan", "Krishna", "Ishaan", "Ananya", "Diya", "Aadhya", "Saanvi",
    "Pari", "Anika", "Navya", "Mira", "Riya", "Kavya",
]

CUSTOMER_LAST_NAMES = [
    "Sharma", "Verma", "Patel", "Gupta", "Reddy", "Nair", "Iyer",
    "Mehta", "Joshi", "Desai", "Khan", "Singh", "Kaur", "Das",
]


def category_names() -> list[str]:
    return [
        f"{department} - {subcategory}"
        for department in DEPARTMENTS
        for subcategory in SUBCATEGORIES
    ]


def product_names() -> list[str]:
    return [
        f"{item} - {variant}"
        for item in PRODUCT_ITEMS
        for variant in PRODUCT_VARIANTS
    ]


def supplier_names() -> list[str]:
    suffixes = [
        "Traders",
        "Distributors",
        "Wholesale",
        "Supply Co",
        "Enterprises",
        "Foods",
        "Mart",
        "Agencies",
        "Logistics",
        "Depot",
    ]
    names = []
    for department in DEPARTMENTS:
        for suffix in suffixes:
            names.append(f"{department} {suffix}")
    return names


def ensure_categories(db: Session) -> list[Category]:
    existing = db.query(Category).order_by(Category.id).all()
    existing_names = {category.name for category in existing}

    for name in category_names():
        if db.query(Category).count() >= TARGET:
            break
        if name in existing_names:
            continue
        category = Category(
            name=name,
            description=f"Demo catalog group for {name.lower()}.",
        )
        db.add(category)
        existing_names.add(name)

    db.flush()
    return db.query(Category).order_by(Category.id).all()


def ensure_products(db: Session, categories: list[Category]) -> list[Product]:
    names = product_names()

    index = 1
    while db.query(Product).count() < TARGET:
        sku = f"DEMO-{index:04d}"
        name = names[(index - 1) % len(names)]
        index += 1

        if db.query(Product).filter(Product.sku == sku).first():
            continue

        # A realistic spread: a few out of stock, a few low, most healthy.
        if index % 23 == 0:
            stock = 0
        elif index % 7 == 0:
            stock = 3
        else:
            stock = 60 + (index * 13) % 240

        reorder_level = 5 + (index * 3) % 21
        price = round(20 + (index * 7.5) % 480, 2)
        category = categories[(index - 1) % len(categories)] if categories else None

        db.add(
            Product(
                name=name,
                sku=sku,
                price=price,
                stock_quantity=stock,
                reorder_level=reorder_level,
                category_id=category.id if category else None,
            )
        )

    db.flush()
    return db.query(Product).order_by(Product.id).all()


def ensure_suppliers(db: Session) -> list[Supplier]:
    names = supplier_names()
    index = 1

    while db.query(Supplier).count() < TARGET:
        name = f"{names[(index - 1) % len(names)]} {index:03d}"
        index += 1

        if db.query(Supplier).filter(Supplier.name == name).first():
            continue

        db.add(
            Supplier(
                name=name,
                email=f"supplier{index:03d}@example.test",
                phone=f"+91-90000-{index:05d}",
                address=f"{index} Market Road, Demo City",
                lead_time_days=1 + (index * 2) % 30,
                performance_rating=round(3.0 + (index % 21) / 10, 1),
            )
        )

    db.flush()
    return db.query(Supplier).order_by(Supplier.id).all()


def demo_products(products: list[Product]) -> list[Product]:
    seeded = [product for product in products if product.sku.startswith("DEMO-")]
    return seeded or products


def ensure_sales_orders(db: Session, products: list[Product]) -> int:
    existing = db.query(Order).count()
    needed = max(0, TARGET - existing)
    if needed == 0:
        return 0

    candidates = [product for product in demo_products(products) if product.stock_quantity > 10]
    if not candidates:
        return 0

    demo_user = db.query(User).order_by(User.id).first()
    created = 0
    for offset in range(needed):
        index = existing + offset + 1
        product = candidates[(index - 1) % len(candidates)]
        quantity = 1 + (index % 5)

        if product.stock_quantity < quantity:
            product = max(candidates, key=lambda item: item.stock_quantity)
            if product.stock_quantity < quantity:
                quantity = 1

        first_name = CUSTOMER_FIRST_NAMES[(index - 1) % len(CUSTOMER_FIRST_NAMES)]
        last_name = CUSTOMER_LAST_NAMES[(index - 1) % len(CUSTOMER_LAST_NAMES)]
        status = SALES_STATUSES[(index - 1) % len(SALES_STATUSES)]

        order = Order(
            customer_name=f"{first_name} {last_name}",
            customer_email=f"customer{index:03d}@example.test",
            product_id=product.id,
            quantity=quantity,
            total_amount=round(product.price * quantity, 2),
            status="Pending",
            user_id=demo_user.id if demo_user else None,
            created_at=datetime.now(timezone.utc)
            - timedelta(
                days=(index * 37) % 365,
                hours=index % 24,
                minutes=(index * 7) % 60,
            ),
        )
        db.add(order)
        db.flush()

        stock_out = change_stock(
            db,
            product,
            "Stock Out",
            quantity,
            f"Sales order #{order.id} created",
        )
        stock_out.created_at = datetime.now(timezone.utc) - timedelta(
            days=(index * 3) % 45,
            hours=index % 24,
        )

        if status == "Cancelled":
            stock_in = change_stock(
                db,
                product,
                "Stock In",
                quantity,
                f"Sales order #{order.id} cancelled",
            )
            stock_in.created_at = stock_out.created_at + timedelta(hours=2)

        order.status = status
        created += 1

    db.flush()
    return created


def ensure_purchase_orders(
    db: Session,
    products: list[Product],
    suppliers: list[Supplier],
) -> int:
    existing = db.query(PurchaseOrder).count()
    needed = max(0, TARGET - existing)
    if needed == 0:
        return 0

    candidates = demo_products(products)
    if not candidates or not suppliers:
        return 0

    created = 0
    for offset in range(needed):
        index = existing + offset + 1
        product = candidates[(index - 1) % len(candidates)]
        supplier = suppliers[(index - 1) % len(suppliers)]
        quantity = 5 + (index * 7) % 60
        unit_price = round(max(1.0, product.price * 0.7), 2)
        status = PURCHASE_STATUSES[(index - 1) % len(PURCHASE_STATUSES)]

        purchase_order = PurchaseOrder(
            supplier_id=supplier.id,
            product_id=product.id,
            quantity=quantity,
            unit_price=unit_price,
            total_amount=round(unit_price * quantity, 2),
            status="Pending",
            created_at=datetime.now(timezone.utc)
            - timedelta(
                days=(index * 29) % 365,
                hours=(index * 5) % 24,
                minutes=(index * 3) % 60,
            ),
        )
        db.add(purchase_order)
        db.flush()

        if status == "Received":
            stock_in = change_stock(
                db,
                product,
                "Stock In",
                quantity,
                f"Purchase order #{purchase_order.id} received",
            )
            stock_in.created_at = datetime.now(timezone.utc) - timedelta(
                days=(index * 2) % 40,
                hours=(index * 5) % 24,
            )

        purchase_order.status = status
        created += 1

    db.flush()
    return created


def ensure_inventory_history(db: Session, products: list[Product]) -> int:
    """Top up inventory history if the order/purchase seed did not reach 100."""
    existing = db.query(InventoryTransaction).count()
    needed = max(0, TARGET - existing)
    if needed == 0:
        return 0

    candidates = [product for product in demo_products(products)]
    if not candidates:
        return 0

    created = 0
    for offset in range(needed):
        product = candidates[offset % len(candidates)]
        quantity = 1 + offset % 10
        transaction = change_stock(
            db,
            product,
            "Stock In",
            quantity,
            "Opening stock adjustment (demo seed)",
        )
        transaction.created_at = datetime.now(timezone.utc) - timedelta(
            days=offset % 30,
            hours=offset % 12,
        )
        created += 1

    db.flush()
    return created


def main() -> None:
    with Session(engine) as db:
        categories = ensure_categories(db)
        products = ensure_products(db, categories)
        suppliers = ensure_suppliers(db)

        orders = ensure_sales_orders(db, products)
        purchase_orders = ensure_purchase_orders(db, products, suppliers)

        # Refresh products after stock movements before topping up history.
        db.flush()
        products = db.query(Product).order_by(Product.id).all()
        history = ensure_inventory_history(db, products)

        db.commit()

        print("Demo data ready")
        print(f"  categories:            {db.query(Category).count()}")
        print(f"  products:              {db.query(Product).count()}")
        print(f"  suppliers:             {db.query(Supplier).count()}")
        print(f"  sales orders:          {db.query(Order).count()} (+{orders})")
        print(f"  purchase orders:       {db.query(PurchaseOrder).count()} (+{purchase_orders})")
        print(f"  inventory history:     {db.query(InventoryTransaction).count()} (+{history})")


if __name__ == "__main__":
    main()
