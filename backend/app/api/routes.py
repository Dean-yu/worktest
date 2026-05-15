from fastapi import APIRouter

from app.models.schemas import ChatRequest, ChatResponse
from app.services.orchestrator import Orchestrator

router = APIRouter()
orchestrator = Orchestrator()


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    return orchestrator.handle(req)
