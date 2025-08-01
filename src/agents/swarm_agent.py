import threading
import time
import uuid

from .protocols import Message, MessageType


class SwarmAgent:
    def __init__(self, message_bus, agent_id=None):
        self.agent_id = agent_id or str(uuid.uuid4())
        self.message_bus = message_bus
        self.state = "idle"
        self.running = False
        self.thread = threading.Thread(target=self._run_loop, daemon=True)

        # Subscribe to direct messages
        self.message_bus.subscribe(
            f"direct.{self.agent_id}", self.handle_direct_message
        )

    def start(self):
        self.running = True
        self.thread.start()
        self.register()

    def stop(self):
        self.running = False

    def _run_loop(self):
        while self.running:
            self.send_heartbeat()
            time.sleep(10)  # Heartbeat interval

    def register(self):
        msg = Message(source_id=self.agent_id, message_type=MessageType.AGENT_REGISTER)
        self.message_bus.publish("system.registration", msg)

    def send_heartbeat(self):
        msg = Message(
            source_id=self.agent_id,
            message_type=MessageType.AGENT_HEARTBEAT,
            payload={"state": self.state},
        )
        self.message_bus.publish("system.heartbeat", msg)

    def handle_direct_message(self, message: Message):
        if message.message_type == MessageType.TASK_ASSIGN:
            threading.Thread(
                target=self.handle_task, args=(message,), daemon=True
            ).start()
        else:
            print(f"[{self.agent_id}] Received direct message: {message.payload}")

    def handle_task(self, task_message: Message):
        self.state = "working"
        print(f"[{self.agent_id}] Started task: {task_message.payload}")
        # Simulate work
        time.sleep(5)
        print(f"[{self.agent_id}] Finished task: {task_message.payload}")
        self.state = "idle"
        completion_msg = Message(
            source_id=self.agent_id,
            target_id=task_message.source_id,
            message_type=MessageType.TASK_COMPLETE,
            payload=task_message.payload,
        )
        self.message_bus.publish("system.task_complete", completion_msg)
