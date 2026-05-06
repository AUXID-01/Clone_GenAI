import webbrowser
import os
from .base import ToolResult
from .registry import registry
from .utils import sanitize_path

def open_in_browser(file_path: str) -> ToolResult:
    """
    Opens the file in the default browser if it exists in the output directory.
    """
    try:
        target_path = sanitize_path(file_path)
            
        if not os.path.exists(target_path):
            return ToolResult(success=False, error=f"File '{file_path}' not found at {target_path}")
        
        webbrowser.open(f"file://{target_path}")
        return ToolResult(success=True, data=f"Opened '{file_path}' in browser.")
    except Exception as e:
        return ToolResult(success=False, error=f"Browser Error: {str(e)}")

# Register tool
registry.register("open_in_browser", open_in_browser)
