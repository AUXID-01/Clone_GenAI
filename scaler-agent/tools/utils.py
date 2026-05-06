import os

def sanitize_path(path: str) -> str:
    """
    Prevents directory traversal attacks and ensures the path is within the output directory.
    """
    base_dir = os.path.abspath("output")
    if not os.path.exists(base_dir):
        os.makedirs(base_dir, exist_ok=True)
    
    # If the path already starts with 'output/', strip it to avoid double-prefixing
    normalized_path = path.replace("\\", "/")
    if normalized_path.startswith("output/"):
        path = path[len("output/"):]
    
    # Normalize path and join with base_dir
    target_path = os.path.abspath(os.path.join(base_dir, path))
    
    if not target_path.startswith(base_dir):
        raise ValueError(f"Access denied: Path '{path}' is outside the sandbox.")
    
    return target_path
