from app.models.schemas import ChatRequest
from app.services.router import RoutePolicy


def test_pick_direct_by_default() -> None:
    req = ChatRequest(user_id="u", session_id="s", message="你好")
    assert RoutePolicy.pick(req) == "direct"


def test_pick_agent_with_keyword() -> None:
    req = ChatRequest(user_id="u", session_id="s", message="帮我规划自动化任务")
    assert RoutePolicy.pick(req) == "agent"


def test_pick_respects_explicit_request_type() -> None:
    req = ChatRequest(user_id="u", session_id="s", message="你好", request_type="agent")
    assert RoutePolicy.pick(req) == "agent"
