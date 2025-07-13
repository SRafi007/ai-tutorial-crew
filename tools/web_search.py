# tools/web_search.py
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
    name: str = "web_search"
    description: str = (
        "Search the web for educational content and extract key information about a topic. "
        "Returns structured content including definitions, concepts, examples, and explanations "
        "that can be used to create comprehensive tutorials."
    )
    args_schema: Type[BaseModel] = SearchInput

    def _run(self, query: str) -> str:
        """Execute the search and return content-focused results"""
        max_retries = 3
        base_delay = 1

        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    delay = base_delay * (2**attempt) + random.uniform(0, 1)
                    time.sleep(delay)

                with DDGS() as ddgs:
                    results = ddgs.text(query, max_results=8)

                    if not results:
                        if attempt < max_retries - 1:
                            continue
                        return f"No results found for the topic: {query}"

                    # Extract and format content
                    content_summary = self._extract_content(results, query)

                    if not content_summary:
                        return f"No relevant educational content found for: {query}"

                    return content_summary

            except Exception as e:
                if attempt < max_retries - 1:
                    continue
                else:
                    return f"Search error: {str(e)}"

        return f"Search failed after {max_retries} attempts"

    def _extract_content(self, results: list, query: str) -> str:
        """Extract and synthesize actual content from search results"""
        if not results:
            return "No content found."

        # Initialize content sections
        content_sections = {
            "definitions": [],
            "key_concepts": [],
            "examples": [],
            "explanations": [],
            "best_practices": [],
        }

        content_output = []
        content_output.append(f"Research Content for: {query}")
        content_output.append("=" * 60)

        for i, result in enumerate(results[:6], 1):
            title = result.get("title", "")
            body = result.get("body", "")
            href = result.get("href", "")

            # Clean the content
            title = self._clean_text(title)
            body = self._clean_text(body)

            # Skip if content is too short
            if len(body) < 50:
                continue

            # Categorize and extract content
            categorized_content = self._categorize_content(title, body)

            if categorized_content:
                content_output.append(f"\n--- Source {i}: {title} ---")
                content_output.append(f"Content: {categorized_content}")
                if href:
                    content_output.append(f"Reference: {href}")

        # Add synthesized summary
        content_output.append("\n" + "=" * 60)
        content_output.append("RESEARCH SUMMARY:")
        content_output.append(self._create_summary(results, query))

        return "\n".join(content_output)

    def _categorize_content(self, title: str, body: str) -> str:
        """Categorize and extract meaningful content"""
        # Look for different types of content
        content_indicators = {
            "definition": [
                "what is",
                "definition",
                "means",
                "refers to",
                "is a",
                "is an",
            ],
            "example": ["example", "for instance", "such as", "like", "including"],
            "explanation": ["how to", "steps", "process", "method", "approach"],
            "benefit": ["advantage", "benefit", "useful", "helpful", "important"],
            "concept": ["concept", "principle", "theory", "idea", "fundamental"],
        }

        full_text = f"{title} {body}".lower()

        # Extract the most relevant content
        if any(
            indicator in full_text for indicator in content_indicators["definition"]
        ):
            return self._extract_definition(body)
        elif any(indicator in full_text for indicator in content_indicators["example"]):
            return self._extract_example(body)
        elif any(
            indicator in full_text for indicator in content_indicators["explanation"]
        ):
            return self._extract_explanation(body)
        else:
            # Return the most informative part
            return self._extract_key_info(body)

    def _extract_definition(self, text: str) -> str:
        """Extract definition-like content"""
        # Look for sentences that contain definitions
        sentences = re.split(r"[.!?]+", text)
        definition_keywords = ["is a", "is an", "refers to", "means", "defined as"]

        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in definition_keywords):
                return sentence.strip()

        return text[:200] + "..." if len(text) > 200 else text

    def _extract_example(self, text: str) -> str:
        """Extract example content"""
        # Look for example-related content
        if "example" in text.lower():
            parts = text.lower().split("example")
            if len(parts) > 1:
                example_part = parts[1][:150]
                return f"Example: {example_part}..."

        return text[:150] + "..." if len(text) > 150 else text

    def _extract_explanation(self, text: str) -> str:
        """Extract explanatory content"""
        # Look for how-to or process content
        process_keywords = ["step", "first", "then", "next", "finally", "process"]

        if any(keyword in text.lower() for keyword in process_keywords):
            return text[:200] + "..." if len(text) > 200 else text

        return text[:150] + "..." if len(text) > 150 else text

    def _extract_key_info(self, text: str) -> str:
        """Extract the most informative content"""
        # Return the first substantial part of the text
        return text[:180] + "..." if len(text) > 180 else text

    def _create_summary(self, results: list, query: str) -> str:
        """Create a synthesized summary of all findings"""
        all_content = []

        for result in results[:5]:
            body = result.get("body", "")
            if body and len(body) > 30:
                all_content.append(self._clean_text(body))

        if not all_content:
            return "No substantial content found for synthesis."

        # Create a basic summary
        summary = f"Based on the research, {query} involves several key aspects:\n\n"

        # Extract common themes (simplified approach)
        combined_text = " ".join(all_content).lower()

        # Look for recurring important terms
        important_terms = self._extract_important_terms(combined_text)

        if important_terms:
            summary += f"Key concepts identified: {', '.join(important_terms[:8])}\n\n"

        summary += "The research indicates this topic covers both theoretical foundations and practical applications. "
        summary += "Multiple sources suggest this is an important area for beginners to understand thoroughly."

        return summary

    def _extract_important_terms(self, text: str) -> list:
        """Extract important terms from the combined text"""
        # Simple keyword extraction (you could use more sophisticated NLP here)
        words = re.findall(r"\b[a-zA-Z]{4,}\b", text)

        # Filter out common words
        stop_words = {
            "that",
            "this",
            "with",
            "from",
            "they",
            "have",
            "were",
            "been",
            "their",
            "said",
            "each",
            "which",
            "then",
            "them",
            "these",
            "will",
            "about",
            "would",
            "there",
            "could",
            "other",
            "more",
            "very",
            "what",
            "know",
            "just",
            "first",
            "also",
            "after",
            "back",
            "work",
            "way",
            "only",
            "new",
            "old",
            "see",
            "him",
            "two",
            "how",
            "its",
            "who",
            "oil",
            "sit",
            "now",
            "find",
            "long",
            "down",
            "day",
            "did",
            "get",
            "has",
            "may",
            "say",
            "she",
            "use",
            "her",
            "all",
            "any",
            "can",
            "had",
            "was",
            "one",
            "our",
            "out",
            "are",
            "but",
            "not",
            "you",
            "all",
            "can",
            "had",
            "her",
            "was",
            "one",
            "our",
            "out",
            "day",
            "get",
            "has",
            "him",
            "his",
            "how",
            "man",
            "new",
            "now",
            "old",
            "see",
            "two",
            "way",
            "who",
            "boy",
            "did",
            "its",
            "let",
            "put",
            "say",
            "she",
            "too",
            "use",
        }

        filtered_words = [word for word in words if word.lower() not in stop_words]

        # Count frequency and return most common
        word_freq = {}
        for word in filtered_words:
            word_freq[word] = word_freq.get(word, 0) + 1

        # Sort by frequency and return top terms
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words if freq > 1][:10]

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        if not text:
            return ""

        # Remove excessive whitespace
        cleaned = re.sub(r"\s+", " ", text)

        # Remove unwanted characters but keep basic punctuation
        cleaned = re.sub(r'[^\w\s\-.,!?;:()\[\]{}"/·&%$#@]', "", cleaned)

        # Remove dates and timestamps
        date_patterns = [
            r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}\b",
            r"\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b",
            r"\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b",
            r"\b\d+\s+(?:hours?|days?|minutes?|seconds?)\s+ago\b",
        ]

        for pattern in date_patterns:
            cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)

        # Remove navigation and UI elements
        ui_patterns = [
            r"\b(?:click|menu|navigation|breadcrumb|sidebar|footer|header)\b",
            r"\b(?:home|contact|about|login|register|subscribe)\b",
            r"\b(?:read more|learn more|continue reading|view all)\b",
        ]

        for pattern in ui_patterns:
            cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)

        # Clean up multiple spaces
        cleaned = re.sub(r"\s+", " ", cleaned)

        return cleaned.strip()


class WebSearchTool:
    @staticmethod
    def tool():
        return DuckDuckGoSearchTool()


# Test the tool
if __name__ == "__main__":
    tool = WebSearchTool.tool()

    print("Testing content-focused web search tool:")
    print("=" * 50)

    # Test with a sample query
    result = tool._run("machine learning basics")
    print(result)
