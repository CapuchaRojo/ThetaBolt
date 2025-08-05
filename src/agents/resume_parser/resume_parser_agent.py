import time
from typing import Any, Dict, List, Optional

from core.protocols import Message, MessageType, Task
from src.agents.base_agent import BaseAgent


class ResumeParserAgent(BaseAgent):
    """A specialized agent for parsing resumes.

    This agent can ingest resume data (e.g., text, PDF) and extract structured
    information such as education, work experience, skills, and contact details.
    """

    def __init__(self, message_bus: Any, agent_id: Optional[str] = None) -> None:
        """Initializes the ResumeParserAgent.

        Args:
            message_bus: The message bus for communication.
            agent_id: The unique identifier for this agent.
        """
        super().__init__(message_bus, agent_id)

    def get_capabilities(self) -> List[str]:
        """Returns a list of task types this agent can handle.

        Returns:
            A list of strings, where each string is a task type.
        """
        return ["resume_parsing"]

    def handle_task(self, task_message: Message) -> None:
        """Handles a resume parsing task.

        Args:
            task_message: The message containing the resume parsing task.
        """
        self.state = "working"
        task: Task = task_message.payload
        print(f"[{self.agent_id}] Started resume parsing task: {task.task_type}")

        # Simulate resume parsing logic
        time.sleep(2)
        parsed_data = {"name": "John Doe", "email": "john.doe@example.com"}
        result = f"Resume parsed successfully: {parsed_data}"

        print(f"[{self.agent_id}] Finished resume parsing task. Result: {result}")
        self.state = "idle"

        completion_payload: Dict[str, Any] = {"original_task": task, "result": result}
        completion_msg: Message = Message(
            source_id=self.agent_id,
            target_id=task_message.source_id,
            message_type=MessageType.TASK_COMPLETE,
            payload=completion_payload,
        )
        self.message_bus.publish("system.task_complete", completion_msg)
