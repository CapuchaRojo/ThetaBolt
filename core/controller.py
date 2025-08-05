from typing import Any, List, Optional

from core.dispatcher import DispatchAgent
from core.message_bus import MessageBus
from src.agents.base_agent import BaseAgent
from src.agents.math_agent import MathAgent
from src.agents.monitor_agent import MonitorAgent
from src.kernel.config_loader import load_config
from src.kernel.quantum_fidelity_kernel import QuantumFidelityKernel
from src.kernel.reservoir_kernel import ReservoirKernel


class Controller:
    """Manages the agent swarm, kernel selection, and overall application lifecycle.

    The Controller is the central orchestration component of the ThetaBolt application.
    It is responsible for initializing the message bus, creating the agent swarm,
    and managing the kernel selection and training process.
    """

    def __init__(self, config: Any = None) -> None:
        """Initializes the Controller.

        Args:
            config: An optional configuration object. If not provided, the configuration
                will be loaded from the default location.
        """
        self.config: Any = config or load_config()
        self.kernel: Optional[Any] = None

        self.message_bus: MessageBus = MessageBus()
        self.dispatch_agent: DispatchAgent = DispatchAgent(self.message_bus)
        self.monitor_agent: MonitorAgent = MonitorAgent(self.message_bus)
        self.swarm: List[BaseAgent] = [
            MathAgent(self.message_bus) for _ in range(self.config.num_agents)
        ]

    def start_swarm(self) -> None:
        """Starts the agent swarm and the dispatch agent."""
        self.dispatch_agent.start()
        for agent in self.swarm:
            agent.start()
        # Add a sample task to the dispatch agent's queue
        from core.protocols import Task

        sample_task = Task(
            task_type="math_task", params={"operation": "add", "values": [10, 20, 30]}
        )
        self.dispatch_agent.add_task(sample_task)

    def stop_swarm(self) -> None:
        """Stops the agent swarm."""
        for agent in self.swarm:
            agent.stop()

    def train(self, X_train: Any, y_train: Any, **kwargs: Any) -> None:
        """Trains the appropriate kernel based on the dataset size.

        Args:
            X_train: The training data.
            y_train: The training labels.
            **kwargs: Additional keyword arguments to pass to the kernel's train method.
        """
        use_quantum: bool = (
            self.config.use_quantum and len(X_train) <= self.config.quantum_threshold
        )

        if use_quantum:
            self.kernel = QuantumFidelityKernel(self.config)
        else:
            self.kernel = ReservoirKernel(self.config)

        self.kernel.train(X_train, y_train, **kwargs)

    def predict(self, X_test: Any) -> Any:
        """Makes predictions using the trained kernel.

        Args:
            X_test: The data to make predictions on.

        Returns:
            The predictions.

        Raises:
            RuntimeError: If the model has not been trained yet.
        """
        if self.kernel is None:
            raise RuntimeError(
                "Model has not been trained yet. Please call train() first."
            )
        return self.kernel.predict(X_test)
