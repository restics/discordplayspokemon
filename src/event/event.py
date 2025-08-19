import asyncio
from collections import defaultdict

# pubsub singleton, pass events as keys 
class EventBus:
    def __init__(self):
        self.events = defaultdict(list)
        
    """
    Publish to a an event topic.
    id: event key to publish to
    eventargs: kwargs that includes details for that event. todo: make this validated w pydantic
    """
    def publish(self, id, **eventargs):
        pass
        

# Abstract class for all events to inherit from
class Event:
    def __init__(self, identifier : str):
        self.identifier = identifier
        
event_bus_instance = EventBus()