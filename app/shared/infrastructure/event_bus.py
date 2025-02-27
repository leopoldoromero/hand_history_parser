import asyncio
from typing import Dict, List, Callable


class EventBus:
    """A simple event bus to allow publishing and subscribing to events."""

    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_name: str, callback: Callable):
        """Subscribe a callback function to an event."""
        print(f"subscribe event::: {event_name}")
        if event_name not in self.subscribers:
            self.subscribers[event_name] = []
        self.subscribers[event_name].append(callback)

    async def publish(self, event_name: str, data: dict):
        """Publish an event and notify all subscribers asynchronously."""
        if event_name in self.subscribers:
            for callback in self.subscribers[event_name]:
                asyncio.create_task(callback(data))


event_bus = EventBus()
