import os
import requests
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

def download_asset(url: str, file_path: str = None) -> ToolResult:
    """
    Downloads a file from a URL and saves it to the specified path within the output directory.
    If file_path is not provided, it attempts to derive one from the URL.
    Uses browser headers to bypass simple bot protection.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        if not file_path:
            # Derive filename from URL
            filename = url.split("/")[-1].split("?")[0]
            if not filename:
                filename = "downloaded_asset"
            file_path = f"assets/{filename}"
            
        sanitized_path = sanitize_path(file_path)
        # Ensure assets directory exists if the path implies it
        os.makedirs(os.path.dirname(sanitized_path), exist_ok=True)
        
        response = requests.get(url, headers=headers, stream=True, timeout=15)
        response.raise_for_status()
        
        with open(sanitized_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return ToolResult(success=True, data=f"Asset downloaded successfully to '{file_path}'.")
    except Exception as e:
        return ToolResult(success=False, error=f"Download failed: {str(e)}")

# Register tools
registry.register("create_folder", create_folder)
registry.register("create_file", create_file)
registry.register("append_file", append_file)
registry.register("read_file", read_file)
registry.register("download_asset", download_asset)
