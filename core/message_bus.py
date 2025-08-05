import fnmatch
from collections import defaultdict
from typing import Any, Callable, Dict, List


class MessageBus:
    """A simple message bus for communication between agents.

    The MessageBus allows agents to publish messages to topics and subscribe to
    topics to receive messages.
    """

    def __init__(self) -> None:
        """Initializes the MessageBus."""
        self.subscriptions: Dict[str, List[Callable]] = defaultdict(list)

    def subscribe(self, topic: str, callback: Callable) -> None:
        """Subscribes a callback to a topic.

        Args:
            topic: The topic to subscribe to.
            callback: The callback to invoke when a message is published to the topic.
        """
        self.subscriptions[topic].append(callback)

    def publish(self, topic: str, message: Any) -> None:
        """Publishes a message to a topic.

        Args:
            topic: The topic to publish the message to.
            message: The message to publish.
        """
        # Direct subscribers
        for callback in self.subscriptions.get(topic, []):
            callback(message)

        # Wildcard subscribers
        for sub_topic, callbacks in self.subscriptions.items():
            if "*" in sub_topic and fnmatch.fnmatch(topic, sub_topic):
                for callback in callbacks:
                    callback(message)