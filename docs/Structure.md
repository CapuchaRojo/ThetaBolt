# ThetaBolt Project Structure & Architecture

This document provides an overview of the ThetaBolt project's directory structure and architectural components.

## Directory Structure

```
ThetaBolt/
├── core/           # Core system components and orchestration logic
│   ├── dispatcher.py       # DispatchAgent core logic and routing
│   ├── controller.py       # High-level governance and "Highlander" selection
│   ├── memory_manager.py   # Deep memory and vector database integration
│   ├── message_bus.py      # Internal messaging and event handling
│   └── protocols.py        # Communication protocols and interfaces
├── src/            # Source code for agents and kernel
│   ├── agents/             # Specialized agent implementations
│   │   ├── resume_parser/  # ResumeParserAgent
│   │   ├── genetic_parser/ # GeneticParserAgent
│   │   ├── granite_agent/  # GraniteAgent
│   │   ├── reflection_agent/# ReflectionAgent
│   │   └── base_agent.py   # Base agent class and utilities
│   ├── kernel/             # Kernel management and configuration
│   └── __init__.py
├── docs/            # Documentation including whitepaper, structure, and manifesto
├── tests/           # Unit and integration tests
├── scripts/         # Utility scripts for setup and maintenance
├── requirements.txt # Production dependencies
├── requirements-dev.txt # Development dependencies
├── README.md        # Project overview and setup instructions
└── LICENSE          # AGPL-3.0 License
```

## Architectural Overview

ThetaBolt is designed as a modular, multi-agent swarm system with the following key components:

- **DispatchAgent**: The central orchestrator responsible for routing tasks and managing agent interactions using interrogative routing and dynamic parser hooks.

- **Controller**: Implements high-level governance logic, including the "Highlander" mechanism to ensure single-instance control where necessary.

- **MemoryManager**: Provides deep memory capabilities through integration with vector databases or file-based semantic search systems, enabling long-term learning and recall.

- **Specialized Agents**: Modular agents each with distinct responsibilities:
  - ResumeParserAgent: Intelligent document parsing.
  - GeneticParserAgent: Optimization via genetic algorithms.
  - GraniteAgent: Core AI processing with quantum-inspired computation.
  - ReflectionAgent: Meta-cognitive agent for critique and system improvement.

- **Kernel**: Manages the core AI kernel lifecycle, configuration, and signal-driven computation.

- **Messaging System**: Internal message bus facilitating communication between agents and core components.

## Development and Testing

- Tests are located in the `tests/` directory and cover unit and integration scenarios.
- CI/CD pipelines include automated testing and coverage reporting.
- Documentation is maintained in the `docs/` directory with detailed guides and whitepapers.

This structure supports extensibility, robustness, and scalability aligned with the project's vision.