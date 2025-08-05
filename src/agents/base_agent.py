import threading
import time
import uuid
from abc import ABC, abstractmethod
from typing import Any, List, Optional

from core.protocols import Message, MessageType


class BaseAgent(ABC):
    """The base class for all agents in the swarm.

    This class provides the basic functionality for an agent, including a unique
    ID, a message bus for communication, a state, and a main loop that runs in a
    separate thread.
    """

    def __init__(self, message_bus: Any, agent_id: Optional[str] = None) -> None:
        """Initializes the BaseAgent.

        Args:
            message_bus: The message bus to use for communication.
            agent_id: An optional unique ID for the agent. If not provided, a new
                ID will be generated.
        """
        self.agent_id: str = agent_id or str(uuid.uuid4())
        self.message_bus: Any = message_bus
        self.state: str = "idle"
        self.running: bool = False
        self.thread: threading.Thread = threading.Thread(
            target=self._run_loop, daemon=True
        )

        # Subscribe to direct messages
        self.message_bus.subscribe(
            f"direct.{self.agent_id}", self.handle_direct_message
        )

    def start(self) -> None:
        """Starts the agent's main loop in a separate thread."""
        self.running = True
        self.thread.start()
        self.register()

    def stop(self) -> None:
        """Stops the agent's main loop."""
        self.running = False

    def _run_loop(self) -> None:
        """The main loop of the agent."""
        while self.running:
            self.send_heartbeat()
            time.sleep(10)  # Heartbeat interval

    def register(self) -> None:
        """Registers the agent with the dispatcher."""
        msg: Message = Message(
            source_id=self.agent_id,
            message_type=MessageType.AGENT_REGISTER,
            payload={"capabilities": self.get_capabilities()},
        )
        self.message_bus.publish("system.registration", msg)

    def send_heartbeat(self) -> None:
        """Sends a heartbeat message to the monitor agent."""
        msg: Message = Message(
            source_id=self.agent_id,
            message_type=MessageType.AGENT_HEARTBEAT,
            payload={"state": self.state},
        )
        self.message_bus.publish("system.heartbeat", msg)

    def handle_direct_message(self, message: Message) -> None:
        """Handles a direct message sent to the agent.

        Args:
            message: The direct message.
        """
        if message.message_type == MessageType.TASK_ASSIGN:
            threading.Thread(
                target=self.handle_task, args=(message,), daemon=True
            ).start()
        else:
            print(f"[{self.agent_id}] Received direct message: {message.payload}")

    @abstractmethod
    def handle_task(self, task_message: Message) -> None:
        """Abstract method to handle an assigned task."""
        pass

    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Abstract method to return a list of task types this agent can handle."""
        pass