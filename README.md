[![CI](https://github.com/CapuchaRojo/ThetaBolt/actions/workflows/ci.yml/badge.svg)](https://github.com/CapuchaRojo/ThetaBolt/actions/workflows/ci.yml)

# ⚡️ ThetaBolt

> _The world's first quantum-inspired AI kernel built for zero-infrastructure autonomy, signal-driven computation, and radical sustainability._

---

## 🔥 What is ThetaBolt?

ThetaBolt is a **quantum-grade agent kernel** engineered to operate without reliance on servers, cloud infra, or data centers. Designed to emulate nature's own feedback loops — like ATP cycles and resonance fields — ThetaBolt delivers intelligent processing through **signal-based logic** and **modular swarm AI**.

Built for performance. Designed for freedom. Powered by the quantum.

---

## 🎯 Project Vision & Architecture

ThetaBolt implements a **multi-agent swarm system** with specialized agents working in concert, orchestrated by a central **Controller**.

- **Controller**: The high-level orchestrator overseeing the entire swarm, managing kernel selection, and implementing "Highlander" logic for result selection.
- **DispatchAgent**: Central orchestrator responsible for intelligent task routing, assigning tasks to specialized agents based on their capabilities, and initiating reflection cycles.
- **ResumeParserAgent**: (Placeholder) Specialized agent for parsing and extracting structured information from resumes.
- **GeneticParserAgent**: (Placeholder) Specialized agent for processing and analyzing genetic or medical data.
- **GraniteAgent**: (Placeholder) Agent designed to interface with external large language models like IBM Granite for advanced AI capabilities.
- **ReflectionAgent**: (Placeholder) Meta-cognitive agent responsible for critiquing agent outputs and feeding observations back for continuous self-improvement.
- **MathAgent**: A proof-of-concept specialized agent for performing mathematical operations.

The system features **deep memory integration** with vector database support for semantic search and long-term learning capabilities, managed by the **MemoryManager**.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Git
- Virtual environment support

### Installation

```bash
# Clone the repository
git clone https://github.com/CapuchaRojo/ThetaBolt.git
cd ThetaBolt

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows, use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements-pinned.txt

# Run tests (with coverage)
pytest --cov=src tests/

# Start the application
python app.py
```

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run pre-commit hooks
pre-commit install

# Generate documentation
cd docs && make html
```

---

## 📚 Documentation

- [Architecture Overview](docs/Structure.md)
- [Whitepaper](docs/Whitepaper.md)
- [Contributing Guidelines](docs/Contributing.md)
- [API Documentation](docs/API.md)

---

## 🛠️ Development

### Project Structure
```
ThetaBolt/
├── app.py          # Main application entrypoint
├── core/           # Core system components (dispatcher, controller, message bus, memory manager, protocols)
│   ├── controller.py
│   ├── dispatcher.py
│   ├── memory_manager.py
│   ├── message_bus.py
│   └── protocols.py
├── src/            # Source code and agents
│   ├── agents/     # Modular agent implementations
│   │   ├── genetic_parser/
│   │   ├── granite_agent/
│   │   ├── math_agent.py
│   │   ├── monitor_agent.py
│   │   ├── reflection_agent/
│   │   └── resume_parser/
│   └── kernel/     # Kernel implementations and configuration
├── docs/           # Project documentation (README, whitepaper, manifesto, etc.)
├── memory/         # Optional: Data directory for memory or embeddings
├── scripts/        # Utility scripts
├── tests/          # Test suite
└── requirements/   # Dependency management (requirements.txt, requirements-pinned.txt)
```

---

## ✨ Core Features

- 🔋 **Self-sustaining Kernel** – Runs on low-power or even energy-harvested environments (e.g. Raspberry Pi, USB, mesh nodes).
- 🧠 **Agent-in-the-Loop Swarm** – Each node acts as a sovereign AI unit capable of learning, routing, and tasking.
- 🧲 **Signal-Aware Computing** – Kernel adapts to real-world inputs: EMF, sound, temperature, and more.
- 🧬 **Deep Memory System** – Persistent learning with vector database integration
- 🔄 **Reflection Cycles** – Continuous self-improvement through meta-cognitive processing
- 🔐 **AGPL-3.0 Licensed** – Ensures the open-source ecosystem remains strong, ethical, and contributive.
- ⚙️ **Drop-in Ready** – Modular design for seamless use across edge devices, field deployments, and simulations.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Git
- Virtual environment support

### Installation

```bash
# Clone the repository
git clone https://github.com/CapuchaRojo/ThetaBolt.git
cd ThetaBolt

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest --cov=src tests/

# Start the application
python -m src.main
```

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run pre-commit hooks
pre-commit install

# Generate documentation
cd docs && make html
```

---

## 📚 Documentation

- [Architecture Overview](docs/Structure.md)
- [Whitepaper](docs/Whitepaper.md)
- [Contributing Guidelines](docs/Contributing.md)
- [API Documentation](docs/API.md)

---

## 🛠️ Development

### Project Structure
```
ThetaBolt/
├── core/           # Core system components
├── src/            # Source code and agents
├── docs/           # Documentation
├── tests/          # Test suite
├── scripts/        # Utility scripts
└── requirements/   # Dependency management
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_swarm_logic.py
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](docs/Contributing.md) for details.

---

## 📄 License

This project is licensed under the AGPL-3.0 License - see the [LICENSE](LICENSE) file for details.
