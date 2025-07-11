from crewai import Agent
from models.local_llm import get_local_llm


class ReviewerAgent:
    def create(self):
        return Agent(
            role="Reviewer",
            goal="Review, refine, and improve tutorials for clarity, grammar, and educational quality",
            backstory=(
                "An experienced technical editor who ensures that tutorials are clear, correct, and well-structured "
                "for readers at all levels, especially beginners."
            ),
            verbose=True,
            llm=get_local_llm(),
            allow_delegation=False,
        )
