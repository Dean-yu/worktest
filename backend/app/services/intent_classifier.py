from app.models.schemas import ClarificationOption, IntentResult


class IntentClassifier:
    """Heuristic intent classifier placeholder for future model-based classification."""

    TASK_KEYWORDS = ("规划", "步骤", "执行", "自动化", "任务", "帮我做", "安排")
    AMBIGUOUS_KEYWORDS = ("帮我", "处理", "搞一下", "看一下", "优化")

    def classify(self, message: str) -> IntentResult:
        text = message.lower().strip()

        if any(keyword in text for keyword in self.TASK_KEYWORDS):
            return IntentResult(route="agent", confidence=0.88, reason="命中任务型关键词")

        if any(keyword in text for keyword in self.AMBIGUOUS_KEYWORDS):
            return IntentResult(
                route="direct",
                confidence=0.55,
                reason="语义存在歧义，需要补充信息",
                needs_clarification=True,
                clarification_question="你希望我直接回答，还是帮你分步骤执行任务？",
                clarification_options=[
                    ClarificationOption(label="直接回答", value="direct"),
                    ClarificationOption(label="分步骤执行", value="agent"),
                    ClarificationOption(label="自定义补充", value="custom"),
                ],
            )

        return IntentResult(route="direct", confidence=0.84, reason="默认按对话问答处理")
