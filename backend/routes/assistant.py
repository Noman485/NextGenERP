from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from assistant.engine import answer_chat
from assistant.localization import refusal_text
from auth.dependencies import get_current_user
from database.connection import engine
from models.user import User
from schemas.assistant import AssistantChatRequest, AssistantChatResponse
from security_controls import check_rate_limit
from services.audit import commit_audit, record_audit

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
    result = answer_chat(
        payload.message,
        db,
        history=[item.model_dump() for item in payload.history],
        language=payload.language,
    )
    if result["reply"] == refusal_text(payload.language):
        # Never copy the prompt itself: it can contain credentials or personal
        # data. Length plus the policy outcome is enough for investigations.
        record_audit(
            db,
            action="assistant.refusal",
            entity_type="assistant",
            actor=current_user,
            outcome="denied",
            after={
                "message_length": len(payload.message),
                "reason": "out_of_scope_or_policy_refusal",
            },
            request=request,
        )
        commit_audit(db)
    return result
