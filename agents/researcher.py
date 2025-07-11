from crewai import Agent
from models.local_llm import get_local_llm, load_yaml_config


class ResearchAgent:
    def create(self):
        config = load_yaml_config()
        a = config["agents"]["researcher"]

        return Agent(
            role=a["role"],
            goal=a["goal"],
            backstory=a["backstory"],
            verbose=True,
            llm=get_local_llm(),
        )
