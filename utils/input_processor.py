# utils/input_processor.py
from models.local_llm import get_local_llm
import re


class InputProcessor:
    def __init__(self):
        self.llm = get_local_llm()

    def process_input(self, raw_input: str) -> str:
        """
        Process raw user input to create a clear, well-formatted topic for tutorial generation.

        Args:
            raw_input (str): Raw user input (potentially broken/unclear)

        Returns:
            str: Clean, formatted topic ready for tutorial generation
        """
        # Clean basic formatting issues
        cleaned_input = self._basic_cleanup(raw_input)

        # If input is already clear and well-formatted, return as-is
        if self._is_clear_input(cleaned_input):
            return cleaned_input

        # Use LLM to fix and clarify the input
        processed_input = self._llm_process(cleaned_input)

        # Final cleanup
        return self._final_cleanup(processed_input)

    def _basic_cleanup(self, text: str) -> str:
        """Basic text cleanup - remove extra spaces, fix common typos"""
        if not text:
            return "Python programming basics"

        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text.strip())

        # Fix common patterns
        text = re.sub(r"\bpython\b", "Python", text, flags=re.IGNORECASE)
        text = re.sub(r"\bjavascript\b", "JavaScript", text, flags=re.IGNORECASE)
        text = re.sub(
            r"\bmachine learn\b", "machine learning", text, flags=re.IGNORECASE
        )
        text = re.sub(r"\bml\b", "machine learning", text, flags=re.IGNORECASE)
        text = re.sub(r"\bai\b", "artificial intelligence", text, flags=re.IGNORECASE)
        text = re.sub(r"\bapi\b", "API", text, flags=re.IGNORECASE)
        text = re.sub(r"\bhtml\b", "HTML", text, flags=re.IGNORECASE)
        text = re.sub(r"\bcss\b", "CSS", text, flags=re.IGNORECASE)
        text = re.sub(r"\bsql\b", "SQL", text, flags=re.IGNORECASE)

        return text

    def _is_clear_input(self, text: str) -> bool:
        """Check if input is already clear and doesn't need LLM processing"""
        # If it's a complete sentence or well-formed topic, likely good to go
        if len(text.split()) >= 3 and (
            text.endswith(".") or self._looks_like_topic(text)
        ):
            return True

        # Common clear patterns
        clear_patterns = [
            r"^[A-Z][a-z]+ (tutorial|guide|basics|introduction)",
            r"^(Learn|Learning) \w+",
            r"^(How to|Getting started with) \w+",
            r"^\w+ (programming|development|fundamentals)",
        ]

        return any(
            re.search(pattern, text, re.IGNORECASE) for pattern in clear_patterns
        )

    def _looks_like_topic(self, text: str) -> bool:
        """Check if text looks like a well-formed topic"""
        # Has proper capitalization and reasonable length
        words = text.split()
        if len(words) < 1 or len(words) > 8:
            return False

        # Check for title case or sentence case
        return text[0].isupper() and len(text) > 5

    def _llm_process(self, text: str) -> str:
        """Use LLM to process and clarify unclear input"""
        prompt = f"""You are a tutorial topic formatter. Your job is to take unclear or broken user input and convert it into a clear, specific tutorial topic.

Rules:
1. Return ONLY the formatted topic, nothing else
2. Make it beginner-friendly and specific
3. Keep it concise (2-6 words typically)
4. Use proper capitalization
5. Focus on the main concept the user wants to learn

Examples:
- "machine learn" → "Machine Learning Basics"
- "python list" → "Python Lists"
- "api rest" → "REST API Development"
- "css style" → "CSS Styling"
- "js function" → "JavaScript Functions"
- "database sql" → "SQL Database Queries"

User input: "{text}"
Formatted topic:"""

        try:
            # Use the correct method for CrewAI LLM
            response = self.llm.call(prompt)

            # Extract the response content
            if hasattr(response, "content"):
                result = response.content.strip()
            else:
                result = str(response).strip()

            # Clean up any extra formatting from LLM response
            result = re.sub(
                r"^(Topic:|Formatted topic:|Answer:)", "", result, flags=re.IGNORECASE
            ).strip()
            result = result.strip("\"'")

            return result if result else text

        except Exception as e:
            print(f"[InputProcessor] LLM processing failed: {e}")
            return text

    def _final_cleanup(self, text: str) -> str:
        """Final cleanup of processed text"""
        # Remove any remaining artifacts
        text = re.sub(r"^\W+|\W+$", "", text)

        # Ensure proper capitalization
        if text and not text[0].isupper():
            text = text[0].upper() + text[1:]

        # Fallback if something went wrong
        if not text or len(text) < 2:
            return "Python Programming Basics"

        return text


# Convenience function for easy import
def process_user_input(raw_input: str) -> str:
    """
    Process raw user input into a clean tutorial topic.

    Args:
        raw_input (str): Raw user input

    Returns:
        str: Processed topic ready for tutorial generation
    """
    processor = InputProcessor()
    return processor.process_input(raw_input)


"""
# Example usage and testing
if __name__ == "__main__":
    # Test cases
    test_inputs = [
        "machine learn",
        "python list",
        "api rest",
        "css style",
        "js function",
        "database sql",
        "Python Lists",  # Already clear
        "Learn React",  # Already clear
        "html",
        "ai",
        "",  # Empty input
        "   machine    learning   ",  # Extra spaces
    ]

    processor = InputProcessor()

    print("Testing Input Processor:")
    print("-" * 50)

    for test_input in test_inputs:
        result = processor.process_input(test_input)
        print(f"Input: '{test_input}' → Output: '{result}'")
"""
