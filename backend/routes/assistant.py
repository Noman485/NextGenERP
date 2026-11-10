from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from assistant.engine import answer_chat
from auth.dependencies import get_current_user
from database.connection import engine
from schemas.assistant import AssistantChatRequest, AssistantChatResponse

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
    db: Session = Depends(get_db),
):
    return answer_chat(
        payload.message,
        db,
        history=[item.model_dump() for item in payload.history],
    )
