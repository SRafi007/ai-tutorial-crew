# _web_search.py
from crewai.tools import BaseTool
from ddgs import DDGS
from typing import Type, Any
from pydantic import BaseModel, Field
import time
import random
import re


class SearchInput(BaseModel):
    """Input schema for DuckDuckGo search."""

    query: str = Field(..., description="The search query to execute")


class DuckDuckGoSearchTool(BaseTool):
    name: str = "_duckduckgo_search"
    description: str = (
        " DuckDuckGo search tool that returns concise, one-line results. "
        "Perfect for AI agents that need quick, readable search summaries."
    )
    args_schema: Type[BaseModel] = SearchInput

    def _run(self, query: str) -> str:
        """Execute the search with , concise formatting"""
        max_retries = 3
        base_delay = 1

        for attempt in range(max_retries):
            try:
                # Add delay for retries
                if attempt > 0:
                    delay = base_delay * (2**attempt) + random.uniform(0, 1)
                    time.sleep(delay)

                with DDGS() as ddgs:
                    results = ddgs.text(query, max_results=8)

                    if not results:
                        if attempt < max_retries - 1:
                            continue
                        return f"No results found for query: {query}"

                    # Filter and format results
                    formatted_results = self._format__results(results)

                    if not formatted_results:
                        return f"No quality results found for query: {query}"

                    return formatted_results

            except Exception as e:
                if attempt < max_retries - 1:
                    continue
                else:
                    return f"Search error for query '{query}': {str(e)}"

        return f"Search failed after {max_retries} attempts for query: {query}"

    def _format__results(self, results: list) -> str:
        """Format results as , one-line summaries matching the desired format"""
        formatted_lines = []

        for result in results:
            title = result.get("title", "")
            body = result.get("body", "")

            #  content
            title = self.__text(title)
            body = self.__text(body)

            # Skip if content is too short
            if len(title) < 10 or len(body) < 30:
                continue

            # Truncate title to reasonable length and add ellipsis
            if len(title) > 55:
                title = title[:52] + "…"

            # Truncate body description
            if len(body) > 120:
                body = body[:117] + "…"

            # Format exactly like the example: "title: description"
            formatted_line = f"{title}: {body}"
            formatted_lines.append(formatted_line)

        return "\n".join(formatted_lines)

    def __text(self, text: str) -> str:
        """and normalize text content"""
        if not text:
            return ""

        # Remove excessive whitespace and normalize
        ed = re.sub(r"\s+", " ", text)

        # Remove unwanted characters but keep basic punctuation
        ed = re.sub(r'[^\w\s\-.,!?;:()\[\]{}"/·]', "", ed)

        # Remove dates and other clutter while preserving content
        date_pattern = r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}\b"
        ed = re.sub(date_pattern, "", ed)

        #  up multiple spaces
        ed = re.sub(r"\s+", " ", ed)

        return ed.strip()


class WebSearchTool:
    @staticmethod
    def tool():
        return DuckDuckGoSearchTool()


"""
# Test the tool
if __name__ == "__main__":
    tool = WebSearchTool.tool()

    print("Testing  web search tool:")
    print("=" * 50)

    # Test with python list comprehension
    result = tool._run("python list comprehension")
    print(result)

    print("\n" + "=" * 50)

    # Test with machine learning
    result = tool._run("machine learning basics")
    print(result)
"""
