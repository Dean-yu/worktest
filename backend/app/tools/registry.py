class ToolRegistry:
    def __init__(self) -> None:
        self._tools = ["web_search", "kb_retrieval", "workflow_executor"]

    def list_tools(self) -> list[str]:
        return self._tools
