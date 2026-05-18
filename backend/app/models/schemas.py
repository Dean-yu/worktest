from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    message: str
    request_type: Optional[Literal["auto", "direct", "agent"]] = "auto"


class ClarificationOption(BaseModel):
    label: str
    value: str


class TaskStep(BaseModel):
    name: str
    status: Literal["pending", "running", "done", "failed"] = "pending"


class ToolEvent(BaseModel):
    tool: str
    status: Literal["start", "success", "error"]
    message: str


class ChatResponse(BaseModel):
    route: Literal["direct", "agent"]
    answer: str
    plan: list[str] = Field(default_factory=list)
    needs_clarification: bool = False
    clarification_question: Optional[str] = None
    clarification_options: list[ClarificationOption] = Field(default_factory=list)
    task_id: Optional[str] = None
    steps: list[TaskStep] = Field(default_factory=list)
    timeline: list[ToolEvent] = Field(default_factory=list)
    can_retry: bool = False


class MemoryItem(BaseModel):
    id: str
    session_id: str
    role: str
    content: str


class MemoryUpdateRequest(BaseModel):
    role: Optional[str] = None
    content: Optional[str] = None


class IntentResult(BaseModel):
    route: Literal["direct", "agent"]
    confidence: float
    reason: str
    needs_clarification: bool = False
    clarification_question: Optional[str] = None
    clarification_options: list[ClarificationOption] = Field(default_factory=list)


class IntentDebug(BaseModel):
    result: IntentResult
    metadata: dict[str, Any] = Field(default_factory=dict)
