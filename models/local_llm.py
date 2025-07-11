# models/local_llm.py
import yaml
from pathlib import Path
from crewai import LLM


def load_yaml_config(path="configs/crew_config.yaml"):
    with open(path, "r") as file:
        return yaml.safe_load(file)


def get_local_llm():
    config = load_yaml_config()
    llm_config = config.get("llm", {})
    model_name = llm_config.get("model", "mistral:latest")
    base_url = llm_config.get("base_url", "http://localhost:11434")

    print(f"[LLM] Loading local model: {model_name} from {base_url}")
    return LLM(model=f"ollama/{model_name}", base_url=base_url)
