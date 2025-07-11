from crewai import Task


class GenerateTutorialTask:
    def create(self, researcher, writer, reviewer):
        return [
            Task(
                description="Research the topic: Python Lists for Beginners.",
                expected_output="Key points and examples about Python lists",
                agent=researcher,
            ),
            Task(
                description="Write a beginner-friendly tutorial using research output.",
                expected_output="Full tutorial in markdown",
                agent=writer,
            ),
            Task(
                description="Review the tutorial for clarity and quality.",
                expected_output="Edited and improved final version",
                agent=reviewer,
            ),
        ]
