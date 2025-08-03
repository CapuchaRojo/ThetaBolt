import threading
import time
import uuid
from typing import Any, Dict, List, Optional, Union

from core.protocols import Message, MessageType, Task


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
        self.register()

    def stop(self) -> None:
        self.running = False

    def _run_loop(self) -> None:
        while self.running:
            self.send_heartbeat()
            time.sleep(10)  # Heartbeat interval

    def register(self) -> None:
        msg: Message = Message(
            source_id=self.agent_id, message_type=MessageType.AGENT_REGISTER
        )
        self.message_bus.publish("system.registration", msg)

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

    def handle_task(self, task_message: Message) -> None:
        self.state = "working"
        task: Task = task_message.payload
        print(f"[{self.agent_id}] Started task: {task.task_type}")

        result: Union[int, str, None] = None
        # Simulate work and perform calculation
        time.sleep(2)
        if task.task_type == "math_task":
            op: Optional[str] = task.params.get("operation")
            values: List[int] = task.params.get("values", [])
            if op == "add":
                result = sum(values)
            elif op == "multiply":
                result = 1
                for v in values:
                    result *= v
            else:
                result = "Unsupported operation"
        else:
            result = "Unknown task type"

        print(
            f"[{self.agent_id}] Finished task: {task.task_type} with result: {result}"
        )
        self.state = "idle"

        completion_payload: Dict[str, Any] = {"original_task": task, "result": result}
        completion_msg: Message = Message(
            source_id=self.agent_id,
            target_id=task_message.source_id,
            message_type=MessageType.TASK_COMPLETE,
            payload=completion_payload,
        )
        self.message_bus.publish("system.task_complete", completion_msg)
