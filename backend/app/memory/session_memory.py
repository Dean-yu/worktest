from collections import defaultdict
from typing import TypedDict
from uuid import uuid4


class Message(TypedDict):
    id: str
    role: str
    content: str


class SessionMemory:
    """In-memory short-term memory with CRUD operations for MVP."""

    def __init__(self, max_history: int = 20) -> None:
        self.max_history = max_history
        self._store: dict[str, list[Message]] = defaultdict(list)

    def load(self, session_id: str) -> list[Message]:
        return self._store[session_id][-self.max_history :]

    def append(self, session_id: str, role: str, content: str) -> Message:
        message: Message = {"id": str(uuid4()), "role": role, "content": content}
        self._store[session_id].append(message)
        return message

    def update(self, session_id: str, message_id: str, role: str | None = None, content: str | None = None) -> Message | None:
        for item in self._store[session_id]:
            if item["id"] == message_id:
                if role is not None:
                    item["role"] = role
                if content is not None:
                    item["content"] = content
                return item
        return None

    def delete(self, session_id: str, message_id: str) -> bool:
        history = self._store[session_id]
        for idx, item in enumerate(history):
            if item["id"] == message_id:
                del history[idx]
                return True
        return False
