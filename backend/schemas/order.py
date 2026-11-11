from pydantic import BaseModel, Field, StrictInt, field_validator

from validation import normalize_email


class CustomerEmailFields(BaseModel):
    customer_email: str | None = None

    @field_validator("customer_email")
    @classmethod
    def validate_customer_email(cls, email: str | None) -> str | None:
        return normalize_email(email)


class OrderCreate(CustomerEmailFields):
    customer_name: str = Field(min_length=1, max_length=200)
    product_id: int
    quantity: StrictInt


class OrderUpdate(CustomerEmailFields):
    customer_name: str = Field(min_length=1, max_length=200)


class OrderStatusUpdate(BaseModel):
    status: str
