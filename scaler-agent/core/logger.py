import logging
import os
from datetime import datetime

class ExecutionLogger:
    def __init__(self, session_id: str = None):
        if not session_id:
            session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        self.log_dir = "logs"
        os.makedirs(self.log_dir, exist_ok=True)
        
        self.log_file = os.path.join(self.log_dir, f"session_{session_id}.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("AgentRuntime")

    def log_step(self, step: str, content: str):
        self.logger.info(f"STEP: {step} | {content}")

    def log_tool(self, tool: str, args: dict, success: bool, result: str):
        status = "SUCCESS" if success else "FAILED"
        self.logger.info(f"TOOL: {tool} | ARGS: {args} | STATUS: {status} | RESULT: {result[:100]}...")

    def log_error(self, error: str):
        self.logger.error(f"RUNTIME ERROR: {error}")

logger = ExecutionLogger()
