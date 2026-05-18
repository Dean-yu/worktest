from uuid import uuid4

from app.memory.session_memory import SessionMemory
from app.models.schemas import ChatRequest, ChatResponse, TaskStep, ToolEvent
from app.services.intent_classifier import IntentClassifier
from app.tools.registry import ToolRegistry


class Orchestrator:
    def __init__(
        self,
        memory: SessionMemory | None = None,
        tools: ToolRegistry | None = None,
        classifier: IntentClassifier | None = None,
    ) -> None:
        self.memory = memory or SessionMemory()
        self.tools = tools or ToolRegistry()
        self.classifier = classifier or IntentClassifier()

    def handle(self, req: ChatRequest) -> ChatResponse:
        history = self.memory.load(req.session_id)

        if req.request_type and req.request_type != "auto":
            route = req.request_type
            intent_needs_clarification = False
            clarification_question = None
            clarification_options = []
        else:
            intent = self.classifier.classify(req.message)
            route = intent.route
            intent_needs_clarification = intent.needs_clarification
            clarification_question = intent.clarification_question
            clarification_options = intent.clarification_options

        if intent_needs_clarification:
            answer = "我可以继续，但需要你先补充关键信息。"
            self.memory.append(req.session_id, "user", req.message)
            self.memory.append(req.session_id, "assistant", answer)
            return ChatResponse(
                route=route,
                answer=answer,
                needs_clarification=True,
                clarification_question=clarification_question,
                clarification_options=clarification_options,
            )

        if route == "direct":
            answer = f"[direct] 已收到：{req.message}（history={len(history)}）"
            return self._respond(req, route="direct", answer=answer)

        plan = ["解析任务目标", "拆分执行步骤", "选择可用工具并执行", "汇总证据并输出结论"]
        tool_names = ", ".join(self.tools.list_tools())
        answer = f"[agent] 已进入任务模式。可用工具：{tool_names}。"
        task_id = str(uuid4())
        steps = [
            TaskStep(name="解析任务目标", status="done"),
            TaskStep(name="拆分执行步骤", status="running"),
            TaskStep(name="选择可用工具并执行", status="pending"),
            TaskStep(name="汇总证据并输出结论", status="pending"),
        ]
        timeline = [
            ToolEvent(tool="planner", status="start", message="已开始规划"),
            ToolEvent(tool="planner", status="success", message="规划完成，准备执行"),
        ]
        return self._respond(req, route="agent", answer=answer, plan=plan, task_id=task_id, steps=steps, timeline=timeline)

    def _respond(
        self,
        req: ChatRequest,
        route: str,
        answer: str,
        plan: list[str] | None = None,
        task_id: str | None = None,
        steps: list[TaskStep] | None = None,
        timeline: list[ToolEvent] | None = None,
        can_retry: bool = False,
    ) -> ChatResponse:
        self.memory.append(req.session_id, "user", req.message)
        self.memory.append(req.session_id, "assistant", answer)
        return ChatResponse(
            route=route,
            answer=answer,
            plan=plan or [],
            task_id=task_id,
            steps=steps or [],
            timeline=timeline or [],
            can_retry=can_retry,
        )
