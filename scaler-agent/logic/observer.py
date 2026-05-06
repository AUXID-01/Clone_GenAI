from core.state import AgentState, TaskStatus
from tools.base import ToolResult
from typing import Dict, Any

class Observer:
    def __init__(self, state: AgentState):
        self.state = state

    def observe(self, tool_name: str, tool_args: Dict[str, Any], result: ToolResult):
        """
        Analyzes the result of a tool execution and updates the agent's internal state.
        """
        # Add to execution history
        self.state.add_trace(
            tool_name=tool_name,
            tool_args=tool_args,
            observation=result.data if result.success else result.error,
            success=result.success
        )
        
        # Logic for auto-detecting task completion based on tool success
        if result.success:
            if tool_name == "create_file":
                file_path = tool_args.get("file_path")
                if file_path and file_path not in self.state.files_generated:
                    self.state.files_generated.append(file_path)
            
            self.state.status = "success"
        else:
            # Handle failure
            self.state.status = "error"
            # Update retry count
            key = f"{tool_name}:{str(tool_args)}"
            self.state.retries[key] = self.state.retries.get(key, 0) + 1

    def get_summary(self) -> str:
        """
        Returns a concise summary of the current state for the LLM.
        """
        completed_tasks = [f"[{t.id}] {t.title}" for t in self.state.tasks if t.status == TaskStatus.COMPLETED]
        pending_tasks = [f"[{t.id}] {t.title}" for t in self.state.tasks if t.status == TaskStatus.PENDING]
        failed_tasks = [f"[{t.id}] {t.title}" for t in self.state.tasks if t.status == TaskStatus.FAILED]
        
        summary = f"OBJECTIVE: {self.state.objective}\n"
        summary += f"Current Phase: {self.state.current_phase}\n"
        summary += f"Files Generated: {', '.join(self.state.files_generated) or 'None'}\n"
        summary += f"Pending Tasks: {', '.join(pending_tasks) or 'None'}\n"
        summary += f"Completed Tasks: {', '.join(completed_tasks) or 'None'}\n"
        if failed_tasks:
            summary += f"Failed Tasks: {', '.join(failed_tasks)}\n"
        
        if self.state.history:
            last_trace = self.state.history[-1]
            summary += f"Last Action: {last_trace.tool_name} ({'Success' if last_trace.success else 'Failed'})"
            if not last_trace.success:
                summary += f"\nLast Error: {last_trace.observation}"
                
        return summary
