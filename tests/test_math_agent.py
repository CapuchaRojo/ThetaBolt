import unittest
from unittest.mock import MagicMock

from core.protocols import Message, MessageType, Task
from src.agents.math_agent import MathAgent


class TestMathAgent(unittest.TestCase):
    """Tests for the MathAgent class."""

    def setUp(self) -> None:
        """Sets up the test environment before each test method."""
        self.message_bus = MagicMock()
        self.agent = MathAgent(self.message_bus, agent_id="math_agent_1")

    def test_handle_task_add(self) -> None:
        """Tests the handle_task method with an 'add' operation."""
        task: Task = Task(
            task_type="math_task", params={"operation": "add", "values": [1, 2, 3]}
        )
        message: Message = Message(
            source_id="dispatcher",
            target_id="math_agent_1",
            message_type=MessageType.TASK_ASSIGN,
            payload=task,
        )
        self.agent.handle_task(message)
        self.message_bus.publish.assert_called_with(
            "system.task_complete", unittest.mock.ANY
        )
        # Check the result in the completion message
        completion_message: Message = self.message_bus.publish.call_args[0][1]
        self.assertEqual(completion_message.payload["result"], 6)

    def test_handle_task_multiply(self) -> None:
        """Tests the handle_task method with a 'multiply' operation."""
        task: Task = Task(
            task_type="math_task", params={"operation": "multiply", "values": [2, 3, 4]}
        )
        message: Message = Message(
            source_id="dispatcher",
            target_id="math_agent_1",
            message_type=MessageType.TASK_ASSIGN,
            payload=task,
        )
        self.agent.handle_task(message)
        self.message_bus.publish.assert_called_with(
            "system.task_complete", unittest.mock.ANY
        )
        # Check the result in the completion message
        completion_message: Message = self.message_bus.publish.call_args[0][1]
        self.assertEqual(completion_message.payload["result"], 24)

    def test_handle_task_unsupported_operation(self) -> None:
        """Tests the handle_task method with an unsupported operation."""
        task: Task = Task(
            task_type="math_task", params={"operation": "subtract", "values": [1, 2, 3]}
        )
        message: Message = Message(
            source_id="dispatcher",
            target_id="math_agent_1",
            message_type=MessageType.TASK_ASSIGN,
            payload=task,
        )
        self.agent.handle_task(message)
        self.message_bus.publish.assert_called_with(
            "system.task_complete", unittest.mock.ANY
        )
        # Check the result in the completion message
        completion_message: Message = self.message_bus.publish.call_args[0][1]
        self.assertEqual(completion_message.payload["result"], "Unsupported operation")

    def test_handle_task_unknown_task_type(self) -> None:
        """Tests the handle_task method with an unknown task type."""
        task: Task = Task(task_type="string_task", params={})
        message: Message = Message(
            source_id="dispatcher",
            target_id="math_agent_1",
            message_type=MessageType.TASK_ASSIGN,
            payload=task,
        )
        self.agent.handle_task(message)
        self.message_bus.publish.assert_called_with(
            "system.task_complete", unittest.mock.ANY
        )
        # Check the result in the completion message
        completion_message: Message = self.message_bus.publish.call_args[0][1]
        self.assertEqual(completion_message.payload["result"], "Unknown task type")
