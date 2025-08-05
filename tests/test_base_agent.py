import unittest
from typing import List
from unittest.mock import MagicMock

from core.protocols import Message, MessageType
from src.agents.base_agent import BaseAgent


class ConcreteAgent(BaseAgent):
    """A concrete implementation of BaseAgent for testing purposes."""

    def get_capabilities(self) -> List[str]:
        """Returns a list of capabilities for the concrete agent."""
        return ["test_capability"]

    def handle_task(self, task_message: Message) -> None:
        """Handles a task for the concrete agent."""
        pass


class TestBaseAgent(unittest.TestCase):
    """Tests for the BaseAgent class."""

    def setUp(self) -> None:
        """Sets up the test environment before each test method."""
        self.message_bus = MagicMock()
        self.agent = ConcreteAgent(self.message_bus, agent_id="test_agent")

    def test_handle_direct_message_other(self) -> None:
        """Tests handling of a direct message with an unsupported message type."""
        message: Message = Message(
            source_id="dispatcher",
            target_id="test_agent",
            message_type=MessageType.DIRECT_MESSAGE,
            payload="test_payload",
        )
        self.agent.handle_direct_message(message)
