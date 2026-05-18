from fastapi import APIRouter, HTTPException

from app.models.schemas import ChatRequest, ChatResponse, MemoryItem, MemoryUpdateRequest
from app.services.orchestrator import Orchestrator

router = APIRouter()
orchestrator = Orchestrator()


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    return orchestrator.handle(req)


@router.get("/memory/{session_id}", response_model=list[MemoryItem])
def list_memory(session_id: str) -> list[MemoryItem]:
    return [MemoryItem(session_id=session_id, **m) for m in orchestrator.memory.load(session_id)]


@router.put("/memory/{session_id}/{message_id}", response_model=MemoryItem)
def update_memory(session_id: str, message_id: str, payload: MemoryUpdateRequest) -> MemoryItem:
    updated = orchestrator.memory.update(session_id, message_id, role=payload.role, content=payload.content)
    if not updated:
        raise HTTPException(status_code=404, detail="memory message not found")
    return MemoryItem(session_id=session_id, **updated)


@router.delete("/memory/{session_id}/{message_id}")
def delete_memory(session_id: str, message_id: str) -> dict:
    deleted = orchestrator.memory.delete(session_id, message_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="memory message not found")
    return {"deleted": True}
