import queue
import threading
import time
from typing import Any, Dict, List

from core.message_bus import MessageBus

from .protocols import Message, MessageType, Task


class DispatchAgent:
    """The DispatchAgent is responsible for routing tasks to available agents.

    It maintains a registry of available agents and their capabilities, and it
    assigns tasks from a queue to the most appropriate agent.
    """

    def __init__(self, message_bus: MessageBus) -> None:
        """Initializes the DispatchAgent.

        Args:
            message_bus: The message bus to use for communication.
        """
        self.message_bus: MessageBus = message_bus
        self.agent_registry: Dict[str, Dict[str, Any]] = {}
        self.specialized_agents: Dict[str, List[str]] = (
            {}
        )  # Maps task_type to agent_ids
        self.task_queue: queue.Queue[Task] = queue.Queue()  # Task queue
        self.running: bool = False
        self.thread: threading.Thread = threading.Thread(
            target=self._run_loop, daemon=True
        )
        self.message_bus.subscribe("system.registration", self.register_agent)
        self.message_bus.subscribe("system.task_complete", self.handle_task_completion)

    def start(self) -> None:
        """Starts the dispatch agent's main loop in a separate thread."""
        self.running = True
        self.thread.start()

    def stop(self) -> None:
        """Stops the dispatch agent's main loop."""
        self.running = False

    def _run_loop(self) -> None:
        """The main loop of the dispatch agent."""
        while self.running:
            self._assign_tasks_from_queue()
            time.sleep(1)  # Check for new tasks and idle agents more frequently

    def add_task(self, task: Task) -> None:
        """Adds a task to the task queue.

        Args:
            task: The task to add.
        """
        self.task_queue.put(task)
        print(f"[Dispatch] Added task to queue: {task.task_type}")

    def register_agent(self, message: Message) -> None:
        """Registers a new agent with the dispatcher.

        Args:
            message: The registration message from the agent.
        """
        agent_id: str = message.source_id
        self.agent_registry[agent_id] = {"state": "idle", "last_heartbeat": time.time()}

        # Register specialized capabilities if provided
        if "capabilities" in message.payload and isinstance(
            message.payload["capabilities"], list
        ):
            for capability in message.payload["capabilities"]:
                if capability not in self.specialized_agents:
                    self.specialized_agents[capability] = []
                self.specialized_agents[capability].append(agent_id)
                print(
                    f"[Dispatch] Agent {agent_id} registered for "
                    f"task type: {capability}"
                )

        print(f"[Dispatch] Registered agent: {agent_id}")

    def handle_task_completion(self, message: Message) -> None:
        """Handles a task completion message from an agent.

        Args:
            message: The task completion message.
        """
        agent_id: str = message.source_id
        if agent_id in self.agent_registry:
            self.agent_registry[agent_id]["state"] = "idle"
            result: Any = message.payload.get("result")
            print(f"[Dispatch] Agent {agent_id} completed task. Result: {result}")

            # Send the completed task to the reflection agent for critique
            critique_msg = Message(
                source_id="dispatch",
                target_id="reflection_agent",
                message_type=MessageType.TASK_CRITIQUE,
                payload=message.payload,
            )
            self.message_bus.publish("direct.reflection_agent", critique_msg)


    def _assign_tasks_from_queue(self) -> None:
        """Assigns tasks from the queue to available agents."""
        if not self.task_queue.empty():
            task = self.task_queue.queue[0]  # Peek at the first task

            # Try to find a specialized agent for the task type
            if task.task_type in self.specialized_agents:
                eligible_agents = self.specialized_agents[task.task_type]
                for agent_id in eligible_agents:
                    if self.agent_registry.get(agent_id, {}).get("state") == "idle":
                        task = self.task_queue.get_nowait()  # Actually get the task
                        task_msg = Message(
                            source_id="dispatch",
                            target_id=agent_id,
                            message_type=MessageType.TASK_ASSIGN,
                            payload=task,
                        )
                        self.message_bus.publish(f"direct.{agent_id}", task_msg)
                        self.agent_registry[agent_id]["state"] = "working"
                        print(
                            f"[Dispatch] Assigned specialized task "
                            f"{task.task_type} to {agent_id}"
                        )
                        return  # Assign one task per loop iteration

            # Fallback: Try to assign to any idle agent
            for agent_id, status in self.agent_registry.items():
                if status["state"] == "idle":
                    try:
                        task = self.task_queue.get_nowait()  # Get task
                        task_msg = Message(
                            source_id="dispatch",
                            target_id=agent_id,
                            message_type=MessageType.TASK_ASSIGN,
                            payload=task,
                        )
                        self.message_bus.publish(f"direct.{agent_id}", task_msg)
                        self.agent_registry[agent_id]["state"] = "working"
                        print(
                            f"[Dispatch] Assigned generic task "
                            f"{task.task_type} to {agent_id}"
                        )
                        return  # Assign one task per loop iteration
                    except queue.Empty:
                        pass  # Queue was empty, no task to assign
            print(
                "[Dispatch] No idle agents available for task, task remains in queue."
            )