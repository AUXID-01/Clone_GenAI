from pydantic import BaseModel
from typing import Any, Optional, Dict

class ToolResult(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = {}

class BaseTool:
    name: str
    description: str
    
    def execute(self, **kwargs) -> ToolResult:
        raise NotImplementedError("Subclasses must implement execute")
