from typing import TypedDict, List, Optional
from langchain_core.messages import BaseMessage

class AgentMathState(TypedDict):
    messages: List[BaseMessage]
    problem: str
    generated_code: Optional[str]
    error_log: Optional[str]
    graph_path: Optional[str]
    retry_count: int