import time
from typing import Any, Dict, List, Optional

from core.protocols import Message, MessageType, Task
from src.agents.base_agent import BaseAgent


class GeneticParserAgent(BaseAgent):
    """A specialized agent for parsing genetic or medical data.

    This agent can ingest genetic sequences, medical reports, or other biomedical
    data and extract relevant patterns, anomalies, or structured information.
    """

    def __init__(self, message_bus: Any, agent_id: Optional[str] = None) -> None:
        """Initializes the GeneticParserAgent.

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
        return ["genetic_data_parsing"]

    def handle_task(self, task_message: Message) -> None:
        """Handles a genetic data parsing task.

        Args:
            task_message: The message containing the genetic data parsing task.
        """
        self.state = "working"
        task: Task = task_message.payload
        print(f"[{self.agent_id}] Started genetic data parsing task: {task.task_type}")

        # Simulate genetic data parsing logic
        time.sleep(2)
        parsed_data = {"gene_sequence": "ATGCGTACG", "mutation_detected": False}
        result = f"Genetic data parsed successfully: {parsed_data}"

        print(f"[{self.agent_id}] Finished genetic data parsing task. Result: {result}")
        self.state = "idle"

        completion_payload: Dict[str, Any] = {"original_task": task, "result": result}
        completion_msg: Message = Message(
            source_id=self.agent_id,
            target_id=task_message.source_id,
            message_type=MessageType.TASK_COMPLETE,
            payload=completion_payload,
        )
        self.message_bus.publish("system.task_complete", completion_msg)
