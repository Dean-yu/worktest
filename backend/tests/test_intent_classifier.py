from app.services.intent_classifier import IntentClassifier


def test_intent_agent() -> None:
    result = IntentClassifier().classify("请帮我规划发布任务")
    assert result.route == "agent"
    assert result.needs_clarification is False


def test_intent_needs_clarification() -> None:
    result = IntentClassifier().classify("帮我看一下")
    assert result.needs_clarification is True
    assert len(result.clarification_options) >= 2
