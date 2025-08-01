import fnmatch
from collections import defaultdict


class MessageBus:
    def __init__(self):
        self.subscriptions = defaultdict(list)

    def subscribe(self, topic, callback):
        self.subscriptions[topic].append(callback)

    def publish(self, topic, message):
        # Direct subscribers
        for callback in self.subscriptions.get(topic, []):
            callback(message)

        # Wildcard subscribers
        for sub_topic, callbacks in self.subscriptions.items():
            if "*" in sub_topic and fnmatch.fnmatch(topic, sub_topic):
                for callback in callbacks:
                    callback(message)
