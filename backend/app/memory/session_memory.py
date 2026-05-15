from collections import defaultdict
from typing import TypedDict


class Message(TypedDict):
    role: str
    content: str


class SessionMemory:
    """In-memory short-term memory for MVP phase."""

    def __init__(self, max_history: int = 20) -> None:
        self.max_history = max_history
        self._store: dict[str, list[Message]] = defaultdict(list)

    def load(self, session_id: str) -> list[Message]:
        return self._store[session_id][-self.max_history :]

    def append(self, session_id: str, role: str, content: str) -> None:
        self._store[session_id].append({"role": role, "content": content})
