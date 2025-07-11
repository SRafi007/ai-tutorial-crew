from crewai import Agent
from models.local_llm import get_local_llm


class WriterAgent:
    def create(self):
        return Agent(
            role="Writer",
            goal="Create easy-to-understand and engaging tutorials based on research",
            backstory=(
                "A professional Python educator and content writer who specializes in "
                "breaking down complex programming topics into simple, structured tutorials."
            ),
            verbose=True,
            llm=get_local_llm(),
            allow_delegation=False,
        )
