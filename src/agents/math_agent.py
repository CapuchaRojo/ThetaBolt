import time
import uuid
from typing import Any, Dict, List, Optional, Union

from core.protocols import Message, MessageType, Task
from src.agents.base_agent import BaseAgent


class MathAgent(BaseAgent):
    """A specialized agent for performing mathematical operations.

    This agent can handle tasks such as addition and multiplication.
    """

    def __init__(self, message_bus: Any, agent_id: Optional[str] = None) -> None:
        """Initializes the MathAgent.

        Args:
            message_bus: The message bus for communication.
            agent_id: The unique identifier for this agent.
        """
        super().__init__(message_bus, agent_id)
        self.agent_id = agent_id or f"math_agent_{uuid.uuid4().hex[:4]}"
        self.register()

    def get_capabilities(self) -> List[str]:
        """Returns a list of task types this agent can handle.

        Returns:
            A list of strings, where each string is a task type.
        """
        return ["math_task"]

    def handle_task(self, task_message: Message) -> None:
        """Handles a mathematical task.

        Args:
            task_message: The message containing the mathematical task.
        """
        self.state = "working"
        task: Task = task_message.payload
        print(f"[{self.agent_id}] Started math task: {task.task_type}")

        result: Union[int, str, None] = None
        time.sleep(1)  # Simulate work
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
            f"[{self.agent_id}] Finished math task: "
            f"{task.task_type} with result: {result}"
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
