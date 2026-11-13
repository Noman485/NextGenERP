from sqlalchemy import CheckConstraint, Column, Float, Integer, String

from database.connection import Base


class Supplier(Base):
    __tablename__ = "suppliers"
    __table_args__ = (
        CheckConstraint(
            "lead_time_days >= 0", name="ck_suppliers_lead_time_non_negative"
        ),
        CheckConstraint(
            "performance_rating IS NULL OR "
            "(performance_rating >= 0 AND performance_rating <= 5)",
            name="ck_suppliers_rating_range",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    lead_time_days = Column(Integer, default=0)
    performance_rating = Column(Float, nullable=True)