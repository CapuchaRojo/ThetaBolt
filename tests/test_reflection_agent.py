import unittest
from unittest.mock import MagicMock

from core.protocols import Message, MessageType, Task
from src.agents.reflection_agent.reflection_agent import ReflectionAgent


class TestReflectionAgent(unittest.TestCase):
    """Tests for the ReflectionAgent class."""

    def setUp(self) -> None:
        """Sets up the test environment before each test method."""
        self.message_bus = MagicMock()
        self.agent = ReflectionAgent(self.message_bus, agent_id="reflection_agent_1")

    def test_handle_task(self) -> None:
        """Tests the handle_task method of the ReflectionAgent."""
        task: Task = Task(task_type="reflection_and_critique", params={})
        message: Message = Message(
            source_id="dispatcher",
            target_id="reflection_agent_1",
            message_type=MessageType.TASK_CRITIQUE,
            payload=task,
        )
        self.agent.handle_task(message)
