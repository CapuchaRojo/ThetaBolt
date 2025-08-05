import time
import unittest
from typing import List

from core.dispatcher import DispatchAgent
from core.message_bus import MessageBus
from core.protocols import Message, MessageType
from src.agents.base_agent import BaseAgent
from src.agents.monitor_agent import MonitorAgent


class TestAgent(BaseAgent):
    """Concrete implementation of BaseAgent for testing purposes."""

    def get_capabilities(self) -> List[str]:
        return ["test_task"]

    def handle_task(self, task_message: Message) -> None:
        self.state = "working"
        # Simulate work
        time.sleep(0.1)
        self.state = "idle"


class TestSwarmLogic(unittest.TestCase):
    """
    Tests for the swarm logic, including agent registration, task assignment,
    and monitoring.
    """

    def setUp(self) -> None:
        """Sets up the test environment before each test method."""
        self.message_bus = MessageBus()
        self.dispatch_agent = DispatchAgent(self.message_bus)
        self.monitor_agent = MonitorAgent(self.message_bus)
        self.agent1 = TestAgent(self.message_bus, agent_id="agent1")
        self.agent2 = TestAgent(self.message_bus, agent_id="agent2")

    def test_agent_registration(self) -> None:
        """Tests that agents can register with the dispatcher."""
        self.agent1.register()
        self.assertIn("agent1", self.dispatch_agent.agent_registry)

    def test_task_assignment_and_completion(self) -> None:
        """Tests that tasks can be assigned to and completed by agents."""
        self.agent1.register()
        self.agent2.register()

        task_payload = {"task": "test_work"}
        task_message = Message(
            message_type=MessageType.TASK_ASSIGN, payload=task_payload
        )
        self.message_bus.publish("dispatch.task", task_message)

        # Wait for the agent to process the task and become idle
        timeout = time.time() + 10  # 10-second timeout
        while (
            self.dispatch_agent.agent_registry["agent1"]["state"] != "idle"
            and time.time() < timeout
        ):
            time.sleep(0.1)

        self.assertEqual(self.dispatch_agent.agent_registry["agent1"]["state"], "idle")

    def test_heartbeat_and_monitoring(self) -> None:
        """Tests that agent heartbeats are monitored correctly."""
        self.agent1.start()
        time.sleep(1)  # Allow time for registration and first heartbeat
        self.agent1.send_heartbeat()
        time.sleep(1)

        summary = self.monitor_agent.get_swarm_health_summary()
        self.assertIn("agent1", summary)
        self.assertEqual(summary["agent1"]["status"], "online")
        self.assertEqual(summary["agent1"]["state"], "idle")

        self.agent1.stop()


if __name__ == "__main__":
    unittest.main()
