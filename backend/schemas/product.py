from pydantic import BaseModel, Field, StrictInt


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    sku: str = Field(min_length=1, max_length=80)
    price: float
    stock_quantity: StrictInt = 0
    reorder_level: int = 10
    category_id: int | None = None