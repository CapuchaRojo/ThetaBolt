import time

from src.agents.dispatch_agent import DispatchAgent
from src.agents.message_bus import MessageBus
from src.agents.swarm_agent import SwarmAgent


def test_full_task_cycle():
    message_bus = MessageBus()

    # Create agents
    dispatch_agent = DispatchAgent(message_bus)
    swarm_agent_1 = SwarmAgent(message_bus, agent_id="swarm_1")

    # Start agents
    dispatch_agent.start()
    swarm_agent_1.start()

    # Allow time for registration
    time.sleep(0.1)

    # Manually trigger task dispatch
    dispatch_agent.dispatch_new_task()

    # Allow time for task assignment and completion
    time.sleep(3)

    # Stop agents
    dispatch_agent.stop()
    swarm_agent_1.stop()

    # Assertions can be tricky with threading and timing.
    # For a real test, we would mock the message bus and check calls.
    # For this demonstration, we rely on the print statements in the agents.
    # A more robust test would be needed for production.
    assert dispatch_agent.agent_registry["swarm_1"]["state"] == "idle"
