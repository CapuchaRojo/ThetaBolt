import fnmatch
from collections import defaultdict
from typing import Any, Callable, Dict, List


class MessageBus:
    def __init__(self) -> None:
        self.subscriptions: Dict[str, List[Callable]] = defaultdict(list)

    def subscribe(self, topic: str, callback: Callable) -> None:
        self.subscriptions[topic].append(callback)

    def publish(self, topic: str, message: Any) -> None:
        # Direct subscribers
        for callback in self.subscriptions.get(topic, []):
            callback(message)

        # Wildcard subscribers
        for sub_topic, callbacks in self.subscriptions.items():
            if "*" in sub_topic and fnmatch.fnmatch(topic, sub_topic):
                for callback in callbacks:
                    callback(message)
