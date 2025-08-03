import time

from core.dispatcher import DispatchAgent
from core.message_bus import MessageBus
from core.protocols import Task
from src.agents.math_agent import MathAgent


def test_full_task_cycle() -> None:
    message_bus = MessageBus()

    # Create agents
    dispatch_agent = DispatchAgent(message_bus)
    swarm_agent_1 = MathAgent(message_bus, agent_id="swarm_1")

    # Start agents
    dispatch_agent.start()
    swarm_agent_1.start()

    # Allow time for registration
    time.sleep(0.1)

    # Manually trigger task dispatch
    dispatch_agent.add_task(
        Task(task_type="math_task", params={"operation": "add", "values": [5, 10]})
    )

    # Allow time for task assignment and completion
    timeout = time.time() + 5  # 5-second timeout
    while (
        dispatch_agent.agent_registry.get("swarm_1", {}).get("state") != "idle"
        and time.time() < timeout
    ):
        time.sleep(0.1)

    # Stop agents
    dispatch_agent.stop()
    swarm_agent_1.stop()

    assert dispatch_agent.agent_registry["swarm_1"]["state"] == "idle"
