from pydantic import BaseModel, Field, StrictInt, field_validator

from validation import normalize_email, normalize_phone


class SupplierCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    lead_time_days: StrictInt = Field(default=0, ge=0)
    performance_rating: float | None = Field(default=None, ge=0, le=5, allow_inf_nan=False)

    @field_validator("name")
    @classmethod
    def validate_name(cls, name: str) -> str:
        name = name.strip()
        if not name:
            raise ValueError("Supplier name is required")
        return name

    @field_validator("email")
    @classmethod
    def validate_email(cls, email: str | None) -> str | None:
        return normalize_email(email)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, phone: str | None) -> str | None:
        return normalize_phone(phone)
