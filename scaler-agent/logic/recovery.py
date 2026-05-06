from core.state import AgentState

class RecoveryManager:
    def __init__(self, state: AgentState):
        self.state = state
        self.max_retries = 3

    def should_retry(self, tool_name: str, tool_args: dict) -> bool:
        key = f"{tool_name}:{str(tool_args)}"
        return self.state.retries.get(key, 0) < self.max_retries

    def get_recovery_instruction(self, tool_name: str, error: str) -> str:
        """
        Provides structural guidance on how to recover from specific errors.
        """
        if "Access denied" in error:
            return "The tool attempted to access a path outside the sandbox. Ensure all paths are relative to the project root or within the 'output' directory."
        if "Validation Error" in error:
            return "The tool arguments were malformed. Verify the required schema and types."
        
        return f"Tool '{tool_name}' failed. Analyze the error and attempt an alternative approach or fix the parameters."
