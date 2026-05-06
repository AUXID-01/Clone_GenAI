import os

def create_folder(folder_path: str) -> str:
    """
    Creates a folder at the given path.
    """
    try:
        os.makedirs(folder_path, exist_ok=True)
        return f"Folder '{folder_path}' created successfully or already exists."
    except Exception as e:
        return f"Error creating folder '{folder_path}': {str(e)}"

def create_file(file_path: str, content: str) -> str:
    """
    Creates a file with the given content, automatically creating parent directories.
    """
    try:
        # Ensure parent directory exists
        parent_dir = os.path.dirname(file_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File '{file_path}' created successfully."
    except Exception as e:
        return f"Error creating file '{file_path}': {str(e)}"

def append_file(file_path: str, content: str) -> str:
    """
    Appends content to an existing file.
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' does not exist. Use create_file first."
        
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(content)
        return f"Content appended to '{file_path}' successfully."
    except Exception as e:
        return f"Error appending to file '{file_path}': {str(e)}"

def read_file(file_path: str) -> str:
    """
    Reads the content of a file.
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' does not exist."
        
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file '{file_path}': {str(e)}"


