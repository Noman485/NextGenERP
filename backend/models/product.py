from sqlalchemy import CheckConstraint, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from database.connection import Base


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        CheckConstraint("price >= 0", name="ck_products_price_non_negative"),
        CheckConstraint(
            "stock_quantity >= 0", name="ck_products_stock_non_negative"
        ),
        CheckConstraint(
            "reorder_level >= 0", name="ck_products_reorder_non_negative"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    sku = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0, nullable=False)
    reorder_level = Column(Integer, default=10, nullable=False)

    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category")