from .registry import registry
# Import tool modules to trigger registration
from . import file_tools
from . import browser_tools
from . import search_tools

# Expose registry for the runtime
__all__ = ["registry"]
