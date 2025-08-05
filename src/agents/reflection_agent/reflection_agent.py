import time
from typing import Any, Dict

from core.protocols import Message, MessageType, Task
from src.agents.base_agent import BaseAgent


class ReflectionAgent(BaseAgent):
    """A specialized agent for performing reflection and critique on completed tasks.

    This agent monitors the outputs of other agents and provides feedback to improve
    their performance.
    """

    def __init__(self, message_bus, agent_id=None):
        """Initializes the ReflectionAgent.

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
        return ["reflection_and_critique"]

    def handle_task(self, task_message: Message) -> None:
        """Handles a reflection and critique task.

        Args:
            task_message: The message containing the task to be critiqued.
        """
        self.state = "working"
        task: Task = task_message.payload
        print(f"[{self.agent_id}] Started reflection and critique task: {task.task_type}")

        # Simulate reflection and critique logic
        time.sleep(1)
        critique_result = "Task completed successfully. No major issues found."
        result = f"Critique: {critique_result}"

        print(f"[{self.agent_id}] Finished reflection and critique task. Result: {result}")
        self.state = "idle"

        completion_payload: Dict[str, Any] = {"original_task": task, "result": result}
        completion_msg: Message = Message(
            source_id=self.agent_id,
            target_id=task_message.source_id,
            message_type=MessageType.TASK_COMPLETE,
            payload=completion_payload,
        )
        self.message_bus.publish("system.task_complete", completion_msg)
