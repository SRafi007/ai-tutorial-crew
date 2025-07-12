# web_search.py
from ddgs import DDGS
from typing import Any, Dict, Optional


class DuckDuckGoSearchTool:
    """Simple tool class that CrewAI can work with"""

    def __init__(self):
        self.name = "duckduckgo_search"
        self.description = (
            "Searches DuckDuckGo for a given query and returns relevant results."
        )
        self.args_schema = {
            "query": {"type": "string", "description": "The search query"}
        }

    def run(self, query: str) -> str:
        """Execute the search"""
        try:
            with DDGS() as ddgs:
                results = ddgs.text(query, max_results=5)
                if not results:
                    return "No results found."

                output = "\n".join([f"{r['title']}: {r['body']}" for r in results])
                return output
        except Exception as e:
            return f"Error performing search: {str(e)}"

    def __call__(self, query: str) -> str:
        """Make the tool callable"""
        return self.run(query)


class WebSearchTool:
    @staticmethod
    def tool():
        return DuckDuckGoSearchTool()


if __name__ == "__main__":
    tool = WebSearchTool.tool()
    print(tool.run("python list comprehension"))
