import os
from .base import ToolResult
from .registry import registry
from .utils import sanitize_path

def create_folder(folder_path: str) -> ToolResult:
    try:
        sanitized_path = sanitize_path(folder_path)
        os.makedirs(sanitized_path, exist_ok=True)
        return ToolResult(success=True, data=f"Folder '{folder_path}' created.")
    except Exception as e:
        return ToolResult(success=False, error=str(e))

def create_file(file_path: str, content: str) -> ToolResult:
    try:
        sanitized_path = sanitize_path(file_path)
        parent_dir = os.path.dirname(sanitized_path)
        os.makedirs(parent_dir, exist_ok=True)
        
        with open(sanitized_path, "w", encoding="utf-8") as f:
            f.write(content)
        return ToolResult(success=True, data=f"File '{file_path}' created.")
    except Exception as e:
        return ToolResult(success=False, error=str(e))

def append_file(file_path: str, content: str) -> ToolResult:
    try:
        sanitized_path = sanitize_path(file_path)
        if not os.path.exists(sanitized_path):
            return ToolResult(success=False, error=f"File '{file_path}' does not exist.")
        
        with open(sanitized_path, "a", encoding="utf-8") as f:
            f.write(content)
        return ToolResult(success=True, data=f"Content appended to '{file_path}'.")
    except Exception as e:
        return ToolResult(success=False, error=str(e))

def read_file(file_path: str) -> ToolResult:
    try:
        sanitized_path = sanitize_path(file_path)
        if not os.path.exists(sanitized_path):
            return ToolResult(success=False, error=f"File '{file_path}' does not exist.")
        
        with open(sanitized_path, "r", encoding="utf-8") as f:
            content = f.read()
        return ToolResult(success=True, data=content)
    except Exception as e:
        return ToolResult(success=False, error=str(e))

# Register tools
registry.register("create_folder", create_folder)
registry.register("create_file", create_file)
registry.register("append_file", append_file)
registry.register("read_file", read_file)
