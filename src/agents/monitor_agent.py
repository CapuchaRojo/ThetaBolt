import time
from typing import Any, Dict

from core.message_bus import MessageBus
from core.protocols import Message


class MonitorAgent:
    """Monitors the health and status of agents in the swarm.

    This agent subscribes to heartbeat messages from other agents and maintains
    a registry of their last known status and state.
    """

    def __init__(self, message_bus: MessageBus) -> None:
        """Initializes the MonitorAgent.

        Args:
            message_bus: The message bus to use for communication.
        """
        self.message_bus: MessageBus = message_bus
        self.agent_health: Dict[str, Dict[str, Any]] = {}
        self.message_bus.subscribe("system.heartbeat", self.update_heartbeat)

    def update_heartbeat(self, message: Message) -> None:
        """Updates the heartbeat for a given agent.

        Args:
            message: The heartbeat message from an agent.
        """
        agent_id: str = message.source_id
        self.agent_health[agent_id] = {
            "last_heartbeat": time.time(),
            "state": message.payload.get("state", "unknown"),
        }

    def get_swarm_health_summary(self) -> Dict[str, Dict[str, str]]:
        """Returns a summary of the health of all agents in the swarm.

        Returns:
            A dictionary where keys are agent IDs and values are dictionaries
            containing the agent's status (online/offline) and state.
        """
        summary: Dict[str, Dict[str, str]] = {}
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
