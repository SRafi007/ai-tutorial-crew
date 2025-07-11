# 🧠 AI Tutorial Crew

A multi-agent system built using [CrewAI](https://github.com/joaomdmoura/crewai) and local LLMs via [Ollama](https://ollama.com). This intelligent team of AI agents collaborates to **research**, **write**, and **review** beginner-friendly Python tutorials automatically.

## ✨ Features

- 🤖 **Multi-agent architecture** - Specialized Researcher, Writer, and Reviewer agents
- 🧠 **Local LLM powered** - Runs on Mistral, Qwen, LLaMA, or other Ollama models
- ⚙️ **YAML-based configuration** - Easy to customize and extend
- 📝 **Markdown output generation** - Clean, structured tutorial files
- 🔐 **Environment variable support** - Secure configuration management
- 🌐 **Extensible design** - Ready for web search tools and API integrations

## 🏗️ Project Structure

```
crewai_python_tutorial_agent/
├── agents/
│   ├── researcher.py       # Research agent implementation
│   ├── writer.py          # Writing agent implementation
│   └── reviewer.py        # Review agent implementation
├── tools/
│   └── web_search.py      # Web search utilities
├── tasks/
│   └── generate_tutorial.py  # Task definitions
├── models/
│   └── local_llm.py       # Local LLM configuration
├── configs/
│   └── crew_config.yaml   # Crew configuration
├── output/                # Generated tutorials
├── main.py               # Main entry point
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
└── README.md            # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.com) installed and running

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-tutorial-crew.git
   cd ai-tutorial-crew
   ```

2. **Install Ollama and pull a model**
   ```bash
   # Install Ollama (if not already installed)
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Pull your preferred model
   ollama pull mistral
   # Or try: ollama pull qwen2 or ollama pull llama3
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configurations
   ```

### Usage

1. **Run the tutorial generation crew**
   ```bash
   python main.py
   ```

2. **Check the output**
   ```bash
   # Generated tutorial will be saved at:
   cat output/python_tutorial.md
   ```

## 📖 How It Works

The system employs three specialized AI agents working in sequence:

1. **🔍 Researcher Agent** - Gathers information about Python concepts and best practices
2. **✍️ Writer Agent** - Creates structured, beginner-friendly tutorial content
3. **📝 Reviewer Agent** - Reviews and improves the tutorial for clarity and accuracy

Each agent uses the local LLM through Ollama to perform their specialized tasks, ensuring privacy and eliminating API costs.

## 🔧 Configuration

Customize the crew behavior by editing `configs/crew_config.yaml`:

```yaml
# Example configuration
agents:
  researcher:
    role: "Python Tutorial Researcher"
    goal: "Research comprehensive Python concepts"
    backstory: "Expert in Python programming..."
  
  writer:
    role: "Tutorial Writer"
    goal: "Create engaging beginner tutorials"
    backstory: "Skilled technical writer..."
```

## 📊 Example Output

```markdown
# Understanding Python Lists: A Beginner's Guide

## What is a List in Python?

A list is a versatile data structure in Python that allows you to store multiple items in a single variable. Lists are ordered, changeable, and allow duplicate values...

## Creating Lists

```python
# Creating a simple list
fruits = ["apple", "banana", "orange"]
print(fruits)  # Output: ['apple', 'banana', 'orange']
```

## Common List Operations

### Adding Items
- `append()` - Add item to end
- `insert()` - Add item at specific position
...
```

## 🛠️ Development

### Adding New Agents

1. Create a new agent file in `agents/`
2. Define the agent's role, goal, and backstory
3. Add the agent to your crew configuration
4. Update `main.py` to include the new agent

### Adding Custom Tools

1. Create tool files in `tools/`
2. Implement your custom functionality
3. Register tools with appropriate agents

## 🔮 Roadmap

- [ ] **Web Search Integration** - Add real-time research capabilities
- [ ] **Multiple Topic Support** - Generate tutorials for various Python topics
- [ ] **Interactive Mode** - Allow users to specify tutorial topics
- [ ] **Output Formats** - Support for HTML, PDF, and other formats
- [ ] **Quality Metrics** - Automated tutorial quality assessment
- [ ] **Unit Tests** - Comprehensive test coverage

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📋 Requirements

- Python 3.8+
- CrewAI
- Ollama
- PyYAML
- python-dotenv

See `requirements.txt` for complete dependencies.

## 🐛 Troubleshooting

### Common Issues

**Ollama not responding:**
```bash
# Check if Ollama is running
ollama list

# Restart Ollama service
ollama serve
```

**Model not found:**
```bash
# Pull the required model
ollama pull mistral
```

**Permission errors:**
```bash
# Ensure output directory exists and is writable
mkdir -p output
chmod 755 output
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewai) - For the amazing multi-agent framework
- [Ollama](https://ollama.com) - For local LLM infrastructure
- The open-source community for inspiration and support

## 📬 Contact

- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

**⭐ If you find this project helpful, please consider giving it a star on GitHub!**