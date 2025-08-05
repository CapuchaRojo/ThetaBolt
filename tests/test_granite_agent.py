import unittest
from unittest.mock import MagicMock

from core.protocols import Message, MessageType, Task
from src.agents.granite_agent.granite_agent import GraniteAgent


class TestGraniteAgent(unittest.TestCase):
    """Tests for the GraniteAgent class."""

    def setUp(self) -> None:
        """Sets up the test environment before each test method."""
        self.message_bus = MagicMock()
        self.agent = GraniteAgent(self.message_bus, agent_id="granite_agent_1")

    def test_handle_task(self) -> None:
        """Tests the handle_task method of the GraniteAgent."""
        task: Task = Task(task_type="granite_llm_interaction", params={})
        message: Message = Message(
            source_id="dispatcher",
            target_id="granite_agent_1",
            message_type=MessageType.TASK_ASSIGN,
            payload=task,
        )
        self.agent.handle_task(message)
