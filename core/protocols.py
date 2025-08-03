import time
import uuid
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, Protocol


class Agent(Protocol):
    def handle_task(self, task_message: "Message") -> None: ...


@dataclass
class Task:
    task_type: str
    params: Dict[str, Any]


class MessageType(Enum):
    # Task-related messages
    TASK_ASSIGN = auto()
    TASK_COMPLETE = auto()
    TASK_FAILED = auto()

    # Status and monitoring
    AGENT_REGISTER = auto()
    AGENT_STATUS_UPDATE = auto()
    AGENT_HEARTBEAT = auto()

    # General communication
    GENERAL_BROADCAST = auto()
    DIRECT_MESSAGE = auto()


@dataclass
class Message:
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source_id: str = "kernel"
    target_id: str = "broadcast"  # Can be agent_id, topic, or 'broadcast'
    message_type: MessageType = MessageType.GENERAL_BROADCAST
    payload: Any = None
    timestamp: float = field(default_factory=time.time)
