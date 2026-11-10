"""Read-only snapshot of the workspace used to ground assistant answers."""

from sqlalchemy import func
from sqlalchemy.orm import Session

from models.order import Order
from models.category import Category
from models.product import Product
from models.purchase_order import PurchaseOrder
from models.supplier import Supplier


def _product_record(product: Product) -> dict:
    return {
        "id": product.id,
        "name": product.name,
        "sku": product.sku,
        "price": float(product.price or 0),
        "stock": int(product.stock_quantity or 0),
        "reorder_level": int(product.reorder_level or 0),
        "category_id": product.category_id,
    }


def _supplier_record(supplier: Supplier) -> dict:
    return {
        "id": supplier.id,
        "name": supplier.name,
        "email": supplier.email,
        "phone": supplier.phone,
        "lead_time_days": int(supplier.lead_time_days or 0),
        "performance_rating": (
            float(supplier.performance_rating)
            if supplier.performance_rating is not None
            else None
        ),
    }


def build_snapshot(db: Session) -> dict:
    products = db.query(Product).order_by(Product.name).limit(200).all()
    suppliers = db.query(Supplier).order_by(Supplier.name).limit(100).all()
    orders = db.query(Order).order_by(Order.id.desc()).limit(20).all()
    purchase_orders = (
        db.query(PurchaseOrder).order_by(PurchaseOrder.id.desc()).limit(20).all()
    )

    product_names = {product.id: product.name for product in products}
    supplier_names = {supplier.id: supplier.name for supplier in suppliers}

    order_counts = dict(
        db.query(Order.status, func.count(Order.id)).group_by(Order.status).all()
    )
    purchase_order_counts = dict(
        db.query(PurchaseOrder.status, func.count(PurchaseOrder.id))
        .group_by(PurchaseOrder.status)
        .all()
    )

    product_records = [_product_record(product) for product in products]
    low_stock = [
        product
        for product in product_records
        if 0 < product["stock"] <= product["reorder_level"]
    ]
    out_of_stock = [
        product for product in product_records if product["stock"] <= 0
    ]

    return {
        "counts": {
            "products": db.query(func.count(Product.id)).scalar() or 0,
            "suppliers": db.query(func.count(Supplier.id)).scalar() or 0,
            "sales_orders": db.query(func.count(Order.id)).scalar() or 0,
            "purchase_orders": db.query(func.count(PurchaseOrder.id)).scalar() or 0,
            "categories": db.query(func.count(Category.id)).scalar() or 0,
        },
        "order_status_counts": order_counts,
        "purchase_order_status_counts": purchase_order_counts,
        "products": product_records,
        "suppliers": [_supplier_record(supplier) for supplier in suppliers],
        "low_stock": sorted(low_stock, key=lambda item: item["stock"]),
        "out_of_stock": out_of_stock,
        "recent_sales_orders": [
            {
                "id": order.id,
                "customer_name": order.customer_name,
                "customer_email": order.customer_email,
                "product_id": order.product_id,
                "product_name": product_names.get(order.product_id),
                "quantity": order.quantity,
                "total_amount": float(order.total_amount or 0),
                "status": order.status,
            }
            for order in orders
        ],
        "recent_purchase_orders": [
            {
                "id": purchase_order.id,
                "supplier_id": purchase_order.supplier_id,
                "supplier_name": supplier_names.get(purchase_order.supplier_id),
                "product_id": purchase_order.product_id,
                "product_name": product_names.get(purchase_order.product_id),
                "quantity": purchase_order.quantity,
                "unit_price": float(purchase_order.unit_price or 0),
                "total_amount": float(purchase_order.total_amount or 0),
                "status": purchase_order.status,
            }
            for purchase_order in purchase_orders
        ],
        "product_names": product_names,
        "supplier_names": supplier_names,
    }


def snapshot_for_llm(snapshot: dict) -> dict:
    """Trim the snapshot so prompts stay small and predictable."""
    return {
        "counts": snapshot["counts"],
        "order_status_counts": snapshot["order_status_counts"],
        "purchase_order_status_counts": snapshot["purchase_order_status_counts"],
        "low_stock": snapshot["low_stock"][:15],
        "out_of_stock": snapshot["out_of_stock"][:15],
        "products": snapshot["products"][:40],
        "suppliers": snapshot["suppliers"][:20],
        "recent_sales_orders": snapshot["recent_sales_orders"][:10],
        "recent_purchase_orders": snapshot["recent_purchase_orders"][:10],
    }
