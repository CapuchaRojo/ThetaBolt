import random
import threading
import time
from typing import Any, Dict

from core.message_bus import MessageBus

from .protocols import Message, MessageType, Task


class DispatchAgent:
    def __init__(self, message_bus: MessageBus) -> None:
        self.message_bus: MessageBus = message_bus
        self.agent_registry: Dict[str, Dict[str, Any]] = {}
        self.running: bool = False
        self.thread: threading.Thread = threading.Thread(
            target=self._run_loop, daemon=True
        )
        self.message_bus.subscribe("system.registration", self.register_agent)
        self.message_bus.subscribe("system.task_complete", self.handle_task_completion)

    def start(self) -> None:
        self.running = True
        self.thread.start()

    def stop(self) -> None:
        self.running = False

    def _run_loop(self) -> None:
        while self.running:
            self.dispatch_new_task()
            time.sleep(15)  # Interval for dispatching new tasks

    def register_agent(self, message: Message) -> None:
        agent_id: str = message.source_id
        self.agent_registry[agent_id] = {"state": "idle", "last_heartbeat": time.time()}
        print(f"[Dispatch] Registered agent: {agent_id}")

    def handle_task_completion(self, message: Message) -> None:
        agent_id: str = message.source_id
        if agent_id in self.agent_registry:
            self.agent_registry[agent_id]["state"] = "idle"
            result: Any = message.payload.get("result")
            print(f"[Dispatch] Agent {agent_id} completed task. Result: {result}")

    def dispatch_new_task(self) -> None:
        # Simple round-robin assignment to idle agents
        for agent_id, status in self.agent_registry.items():
            if status["state"] == "idle":
                # Create a random math task
                task = Task(
                    task_type="math_task",
                    params={
                        "operation": random.choice(["add", "multiply"]),
                        "values": [
                            random.randint(1, 100) for _ in range(random.randint(2, 5))
                        ],
                    },
                )
                task_msg = Message(
                    source_id="dispatch",
                    target_id=agent_id,
                    message_type=MessageType.TASK_ASSIGN,
                    payload=task,
                )
                self.message_bus.publish(f"direct.{agent_id}", task_msg)
                self.agent_registry[agent_id]["state"] = "working"
                print(f"[Dispatch] Assigned task {task.task_type} to {agent_id}")
                return
        print("[Dispatch] No idle agents available for new task.")
