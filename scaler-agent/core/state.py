from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class Task(BaseModel):
    id: str
    title: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    dependencies: List[str] = []
    result: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

class ToolTrace(BaseModel):
    tool_name: str
    tool_args: Dict[str, Any]
    observation: str
    success: bool
    timestamp: datetime = Field(default_factory=datetime.now)

class AgentState(BaseModel):
    objective: str
    current_phase: str = "initialization"
    tasks: List[Task] = []
    history: List[ToolTrace] = []
    files_generated: List[str] = []
    retries: Dict[str, int] = {}
    status: str = "idle"
    
    def get_pending_tasks(self) -> List[Task]:
        return [t for t in self.tasks if t.status == TaskStatus.PENDING]
    
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        for t in self.tasks:
            if t.id == task_id:
                return t
        return None

    def update_task(self, task_id: str, status: TaskStatus, result: str = None):
        task = self.get_task_by_id(task_id)
        if task:
            task.status = status
            task.result = result
            if status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
                task.completed_at = datetime.now()

    def add_trace(self, tool_name: str, tool_args: Dict[str, Any], observation: str, success: bool):
        self.history.append(ToolTrace(
            tool_name=tool_name,
            tool_args=tool_args,
            observation=observation,
            success=success
        ))
