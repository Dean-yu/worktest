from app.models.schemas import ChatRequest


class RoutePolicy:
    """Starter policy for direct/agent routing."""

    TASK_KEYWORDS = ("规划", "plan", "步骤", "执行", "自动化", "调用工具", "任务")

    @classmethod
    def pick(cls, req: ChatRequest) -> str:
        if req.request_type and req.request_type != "auto":
            return req.request_type

        text = req.message.lower()
        if any(keyword in text for keyword in cls.TASK_KEYWORDS):
            return "agent"
        return "direct"
