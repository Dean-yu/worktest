from app.models.schemas import ChatRequest
from app.services.orchestrator import Orchestrator


def test_orchestrator_direct_path_and_memory_growth() -> None:
    orchestrator = Orchestrator()
    req = ChatRequest(user_id="u", session_id="s1", message="你好")

    resp = orchestrator.handle(req)

    assert resp.route == "direct"
    assert resp.plan == []
    history = orchestrator.memory.load("s1")
    assert len(history) == 2


def test_orchestrator_agent_path_returns_plan() -> None:
    orchestrator = Orchestrator()
    req = ChatRequest(user_id="u", session_id="s2", message="帮我规划部署任务")

    resp = orchestrator.handle(req)

    assert resp.route == "agent"
    assert len(resp.plan) == 4
    assert "可用工具" in resp.answer


def test_orchestrator_clarification_response() -> None:
    orchestrator = Orchestrator()
    req = ChatRequest(user_id="u", session_id="s3", message="帮我看一下这个")

    resp = orchestrator.handle(req)

    assert resp.needs_clarification is True
    assert resp.clarification_question is not None
    assert len(resp.clarification_options) >= 2


def test_orchestrator_agent_task_payload() -> None:
    orchestrator = Orchestrator()
    req = ChatRequest(user_id="u", session_id="s4", message="请帮我执行发布任务")

    resp = orchestrator.handle(req)

    assert resp.task_id is not None
    assert len(resp.steps) == 4
    assert len(resp.timeline) >= 1
