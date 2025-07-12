# main.py
from crewai import Crew
from agents.researcher import ResearchAgent
from agents.writer import WriterAgent
from agents.reviewer import ReviewerAgent
from tasks.generate_tutorial import GenerateTutorialTask
import os
from models.local_llm import get_local_llm


OUTPUT_DIR = "output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "python_tutorial.md")


def save_output_to_file(content):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        # Handle CrewOutput object - extract the raw content
        if hasattr(content, "raw"):
            f.write(str(content.raw))
        else:
            f.write(str(content))


def run(topic="Python Lists"):
    llm = get_local_llm()

    researcher = ResearchAgent().create()
    writer = WriterAgent().create()
    reviewer = ReviewerAgent().create()

    # Apply LLM override
    researcher.llm = llm
    writer.llm = llm
    reviewer.llm = llm

    # Pass topic to task generator
    tasks = GenerateTutorialTask().create(researcher, writer, reviewer, topic)

    crew = Crew(agents=[researcher, writer, reviewer], tasks=tasks, verbose=True)

    print(f"\n🚀 Running your AI Tutorial Team for topic: {topic}...\n")
    result = crew.kickoff()

    print("\n📘 Final Output:\n")
    print(result)

    save_output_to_file(result)
    print(f"\n✅ Output saved to {OUTPUT_FILE}")


"""
if __name__ == "__main__":
    run()
"""
