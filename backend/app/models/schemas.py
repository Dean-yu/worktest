from typing import Literal, Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    message: str
    request_type: Optional[Literal["auto", "direct", "agent"]] = "auto"


class ChatResponse(BaseModel):
    route: Literal["direct", "agent"]
    answer: str
    plan: list[str] = Field(default_factory=list)
