import unittest
from unittest.mock import MagicMock

from core.protocols import Message, MessageType, Task
from src.agents.resume_parser.resume_parser_agent import ResumeParserAgent


class TestResumeParserAgent(unittest.TestCase):
    """Tests for the ResumeParserAgent class."""

    def setUp(self):
        """Sets up the test environment before each test method."""
        self.message_bus = MagicMock()
        self.agent = ResumeParserAgent(self.message_bus, agent_id="resume_parser_agent_1")

    def test_handle_task(self):
        """Tests the handle_task method of the ResumeParserAgent."""
        task = Task(task_type="resume_parsing", params={})
        message = Message(source_id="dispatcher", target_id="resume_parser_agent_1", message_type=MessageType.TASK_ASSIGN, payload=task)
        self.agent.handle_task(message)