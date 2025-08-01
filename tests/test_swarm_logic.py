import time
import unittest

from src.agents.dispatch_agent import DispatchAgent
from src.agents.message_bus import MessageBus
from src.agents.monitor_agent import MonitorAgent
from src.agents.protocols import Message, MessageType
from src.agents.swarm_agent import SwarmAgent


class TestSwarmLogic(unittest.TestCase):

    def setUp(self):
        self.message_bus = MessageBus()
        self.dispatch_agent = DispatchAgent(self.message_bus)
        self.monitor_agent = MonitorAgent(self.message_bus)
        self.agent1 = SwarmAgent(self.message_bus, agent_id="agent1")
        self.agent2 = SwarmAgent(self.message_bus, agent_id="agent2")

    def test_agent_registration(self):
        self.agent1.register()
        self.assertIn("agent1", self.dispatch_agent.agent_registry)

    def test_task_assignment_and_completion(self):
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

    def test_heartbeat_and_monitoring(self):
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
