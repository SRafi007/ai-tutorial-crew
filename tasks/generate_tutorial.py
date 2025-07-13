# tasks/generate_tutorial.py
from crewai import Task


class GenerateTutorialTask:
    def create(self, researcher, writer, reviewer, topic: str):
        return [
            Task(
                description=f"Research the topic: {topic}.",
                expected_output=f"Key points and examples about {topic.lower()}",
                agent=researcher,
            ),
            Task(
                description=f"Write a beginner-friendly tutorial on {topic} using research output.",
                expected_output=f"Full tutorial on {topic} in markdown format",
                agent=writer,
            ),
            Task(
                description=f"Review the {topic} tutorial for clarity and quality.",
                expected_output="Edited and improved final version",
                agent=reviewer,
            ),
        ]
