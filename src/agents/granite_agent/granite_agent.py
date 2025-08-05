import time
from typing import Any, Dict

from core.protocols import Message, MessageType, Task
from src.agents.base_agent import BaseAgent


class GraniteAgent(BaseAgent):
    """A specialized agent for interacting with IBM Granite LLM.

    This agent acts as a wrapper to call IBM's Granite LLM (via API) for tasks
    requiring complex queries or large text analysis.
    """

    def __init__(self, message_bus, agent_id=None):
        """Initializes the GraniteAgent.

        Args:
            message_bus: The message bus for communication.
            agent_id: The unique identifier for this agent.
        """
        super().__init__(message_bus, agent_id)

    def get_capabilities(self):
        """Returns a list of task types this agent can handle.

        Returns:
            A list of strings, where each string is a task type.
        """
        return ["granite_llm_interaction"]

    def handle_task(self, task_message: Message) -> None:
        """Handles a task for interacting with IBM Granite LLM.

        Args:
            task_message: The message containing the task for Granite LLM.
        """
        self.state = "working"
        task: Task = task_message.payload
        print(f"[{self.agent_id}] Started Granite LLM interaction task: {task.task_type}")

        # Simulate IBM Granite LLM interaction logic
        time.sleep(3)
        llm_response = "This is a simulated response from IBM Granite LLM."
        result = f"Granite LLM interaction successful: {llm_response}"

        print(f"[{self.agent_id}] Finished Granite LLM interaction task. Result: {result}")
        self.state = "idle"

        completion_payload: Dict[str, Any] = {"original_task": task, "result": result}
        completion_msg: Message = Message(
            source_id=self.agent_id,
            target_id=task_message.source_id,
            message_type=MessageType.TASK_COMPLETE,
            payload=completion_payload,
        )
        self.message_bus.publish("system.task_complete", completion_msg)
