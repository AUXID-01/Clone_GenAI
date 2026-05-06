import requests
import warnings
from duckduckgo_search import DDGS
from .base import ToolResult
from .registry import registry

# Suppress the library's internal rename warning
warnings.filterwarnings("ignore", message="This package .* has been renamed to `ddgs`")

def web_search(query: str) -> ToolResult:
    """
    Performs a web search to find information or asset URLs.
    Returns results as a string to ensure compatibility with state models.
    """
    try:
        results = []
        with DDGS() as ddgs:
            # Try with a timeout and max results
            for r in ddgs.text(query, max_results=5):
                results.append(f"Title: {r['title']}\nLink: {r['href']}\nSnippet: {r['body']}\n---")
        
        if not results:
            return ToolResult(success=True, data="No results found for your query.")
            
        return ToolResult(success=True, data="\n".join(results))
    except Exception as e:
        return ToolResult(success=False, error=f"Search failed: {str(e)}")

def fetch_web_content(url: str) -> ToolResult:
    """
    Fetches the text content of a URL for extraction with browser headers.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return ToolResult(success=True, data=response.text[:12000]) # Slightly more context
    except Exception as e:
        return ToolResult(success=False, error=f"Fetch failed: {str(e)}")

# Register tools
registry.register("web_search", web_search)
registry.register("fetch_web_content", fetch_web_content)
