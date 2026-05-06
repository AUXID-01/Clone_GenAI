import webbrowser
import os

def open_in_browser(file_path: str) -> str:
    """
    Converts path to absolute and opens it in the default browser.
    """
    try:
        abs_path = os.path.abspath(file_path)
        if not os.path.exists(abs_path):
            return f"Error: File '{file_path}' does not exist at {abs_path}"
        
        webbrowser.open(f"file://{abs_path}")
        return f"Opened '{file_path}' in browser."
    except Exception as e:
        return f"Error opening browser: {str(e)}"
