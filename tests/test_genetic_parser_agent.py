import unittest
from unittest.mock import MagicMock

from core.protocols import Message, MessageType, Task
from src.agents.genetic_parser.genetic_parser_agent import GeneticParserAgent


class TestGeneticParserAgent(unittest.TestCase):
    """Tests for the GeneticParserAgent class."""

    def setUp(self) -> None:
        """Sets up the test environment before each test method."""
        self.message_bus = MagicMock()
        self.agent = GeneticParserAgent(
            self.message_bus, agent_id="genetic_parser_agent_1"
        )

    def test_handle_task(self) -> None:
        """Tests the handle_task method of the GeneticParserAgent."""
        task: Task = Task(task_type="genetic_data_parsing", params={})
        message: Message = Message(
            source_id="dispatcher",
            target_id="genetic_parser_agent_1",
            message_type=MessageType.TASK_ASSIGN,
            payload=task,
        )
        self.agent.handle_task(message)
