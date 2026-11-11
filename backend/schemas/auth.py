from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from validation import normalize_email


class Credentials(BaseModel):
    username: str = Field(min_length=3, max_length=80, pattern=r"^[A-Za-z0-9_.-]+$")
    password: str = Field(min_length=12, max_length=128)


class UserRegistration(Credentials):
    email: str | None = Field(default=None, max_length=255)

    @field_validator("email")
    @classmethod
    def validate_email(cls, email: str | None) -> str | None:
        return normalize_email(email)


class UserLogin(BaseModel):
    username: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=1, max_length=128)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str | None = None
    role: str = "USER"
    is_active: bool = True
    created_at: datetime | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
