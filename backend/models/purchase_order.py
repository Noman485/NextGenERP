from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import relationship

from database.connection import Base

PURCHASE_ORDER_STATUSES = (
    "Pending",
    "Approved",
    "Ordered",
    "Received",
    "Cancelled",
)


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    __table_args__ = (
        CheckConstraint(
            "quantity > 0", name="ck_purchase_orders_quantity_positive"
        ),
        CheckConstraint(
            "unit_price >= 0", name="ck_purchase_orders_unit_price_non_negative"
        ),
        CheckConstraint(
            "total_amount >= 0",
            name="ck_purchase_orders_total_non_negative",
        ),
        CheckConstraint(
            "status IN ('Pending', 'Approved', 'Ordered', 'Received', 'Cancelled')",
            name="ck_purchase_orders_status_valid",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String, default="Pending", nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=True,
        server_default=func.now(),
        index=True,
    )

    supplier = relationship("Supplier")
    product = relationship("Product")