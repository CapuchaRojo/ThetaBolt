import threading
import time
import uuid
from typing import Any, List, Optional

from core.protocols import Message, MessageType


class BaseAgent:
    def __init__(self, message_bus: Any, agent_id: Optional[str] = None) -> None:
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
        self.running = True
        self.thread.start()

    def stop(self) -> None:
        self.running = False

    def _run_loop(self) -> None:
        while self.running:
            self.send_heartbeat()
            time.sleep(10)  # Heartbeat interval

    def register(self) -> None:
        msg: Message = Message(
            source_id=self.agent_id,
            message_type=MessageType.AGENT_REGISTER,
            payload={"capabilities": self.get_capabilities()},
        )
        self.message_bus.publish("system.registration", msg)

    def get_capabilities(self) -> List[str]:
        """Returns a list of task types this agent can handle."""
        return []  # Default to no specific capabilities

    def send_heartbeat(self) -> None:
        msg: Message = Message(
            source_id=self.agent_id,
            message_type=MessageType.AGENT_HEARTBEAT,
            payload={"state": self.state},
        )
        self.message_bus.publish("system.heartbeat", msg)

    def handle_direct_message(self, message: Message) -> None:
        if message.message_type == MessageType.TASK_ASSIGN:
            threading.Thread(
                target=self.handle_task, args=(message,), daemon=True
            ).start()
        else:
            print(f"[{self.agent_id}] Received direct message: {message.payload}")
