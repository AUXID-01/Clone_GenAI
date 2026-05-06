import requests
from duckduckgo_search import DDGS
from .base import ToolResult
from .registry import registry

def web_search(query: str) -> ToolResult:
    """
    Performs a web search to find information or asset URLs.
    """
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=5):
                results.append({
                    "title": r['title'],
                    "link": r['href'],
                    "snippet": r['body']
                })
        
        if not results:
            return ToolResult(success=True, data="No results found for your query.")
            
        return ToolResult(success=True, data=results)
    except Exception as e:
        return ToolResult(success=False, error=f"Search failed: {str(e)}")

def fetch_web_content(url: str) -> ToolResult:
    """
    Fetches the text content of a URL for extraction.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        # Return truncated content to stay within token limits but provide enough for extraction
        return ToolResult(success=True, data=response.text[:10000])
    except Exception as e:
        return ToolResult(success=False, error=f"Fetch failed: {str(e)}")

# Register tools
registry.register("web_search", web_search)
registry.register("fetch_web_content", fetch_web_content)
