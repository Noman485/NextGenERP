from pydantic import BaseModel, Field, field_validator


class AssistantHistoryItem(BaseModel):
    role: str
    content: str = Field(min_length=1, max_length=2000)

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: str) -> str:
        if value not in {"user", "assistant"}:
            raise ValueError("Role must be user or assistant")
        return value


class AssistantChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)
    history: list[AssistantHistoryItem] = Field(default_factory=list, max_length=10)

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Message is required")
        return value


class AssistantChatResponse(BaseModel):
    reply: str
    suggestions: list[str]
    mode: str
