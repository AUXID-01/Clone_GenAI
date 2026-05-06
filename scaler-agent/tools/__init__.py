from .file_tools import create_file, create_folder, append_file, read_file
from .browser_tools import open_in_browser

tool_map = {
    "create_folder": create_folder,
    "create_file": create_file,
    "append_file": append_file,
    "read_file": read_file,
    "open_in_browser": open_in_browser
}


