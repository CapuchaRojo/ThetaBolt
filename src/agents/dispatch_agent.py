import time

from .message_bus import MessageBus
from .protocols import Message, MessageType


class DispatchAgent:
    def __init__(self, message_bus: MessageBus):
        self.message_bus = message_bus
        self.agent_registry = {}
        self.message_bus.subscribe("system.registration", self.register_agent)
        self.message_bus.subscribe("dispatch.task", self.assign_task)
        self.message_bus.subscribe("system.task_complete", self.handle_task_completion)

    def register_agent(self, message: Message):
        agent_id = message.source_id
        self.agent_registry[agent_id] = {"state": "idle", "last_heartbeat": time.time()}
        print(f"[Dispatch] Registered agent: {agent_id}")

    def handle_task_completion(self, message: Message):
        agent_id = message.source_id
        if agent_id in self.agent_registry:
            self.agent_registry[agent_id]["state"] = "idle"
            print(f"[Dispatch] Agent {agent_id} completed task.")

    def assign_task(self, message: Message):
        # Simple round-robin assignment to idle agents
        for agent_id, status in self.agent_registry.items():
            if status["state"] == "idle":
                task_msg = Message(
                    source_id="dispatch",
                    target_id=agent_id,
                    message_type=MessageType.TASK_ASSIGN,
                    payload=message.payload,
                )
                self.message_bus.publish(f"direct.{agent_id}", task_msg)
                self.agent_registry[agent_id]["state"] = "working"
                print(f"[Dispatch] Assigned task to {agent_id}")
                return
        print("[Dispatch] No idle agents available for task.")
