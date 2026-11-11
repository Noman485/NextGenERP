from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from assistant.engine import answer_chat
from auth.dependencies import get_current_user
from database.connection import engine
from models.user import User
from schemas.assistant import AssistantChatRequest, AssistantChatResponse
from security_controls import check_rate_limit

router = APIRouter(
    prefix="/assistant",
    tags=["Assistant"],
    dependencies=[Depends(get_current_user)],
)


def get_db():
    with Session(engine) as session:
        yield session


@router.post("/chat", response_model=AssistantChatResponse)
def chat(
    payload: AssistantChatRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    check_rate_limit(request, "assistant", identity=str(current_user.id))
    return answer_chat(
        payload.message,
        db,
        history=[item.model_dump() for item in payload.history],
        language=payload.language,
    )
