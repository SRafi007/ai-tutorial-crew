# agents/reviewer.py
from crewai import Agent
from models.local_llm import get_local_llm, load_yaml_config


class ReviewerAgent:
    def create(self):
        config = load_yaml_config()
        a = config["agents"]["reviewer"]

        return Agent(
            role=a["role"],
            goal=a["goal"],
            backstory=a["backstory"],
            verbose=True,
            llm=get_local_llm(),
            allow_delegation=False,
        )
