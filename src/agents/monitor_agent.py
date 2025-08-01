import time

from .message_bus import MessageBus
from .protocols import Message


class MonitorAgent:
    def __init__(self, message_bus: MessageBus):
        self.message_bus = message_bus
        self.agent_health = {}
        self.message_bus.subscribe("system.heartbeat", self.update_heartbeat)

    def update_heartbeat(self, message: Message):
        agent_id = message.source_id
        self.agent_health[agent_id] = {
            "last_heartbeat": time.time(),
            "state": message.payload.get("state", "unknown"),
        }

    def get_swarm_health_summary(self):
        summary = {}
        for agent_id, health_data in self.agent_health.items():
            summary[agent_id] = {
                "status": (
                    "online"
                    if (time.time() - health_data["last_heartbeat"]) < 15
                    else "offline"
                ),
                "state": health_data["state"],
            }
        return summary
