from singleton.singleton import Singleton
from event import Event
from loggingg.config import logger

class EventPublisher(Singleton):
    def __init__(self,debug=False):
        self.listeners:dict={}
        self.debug=debug
        
    def publish(self,event:Event):
        event_type = event.__class__.__name__
        if event_type in self.listeners:
            for method in self.listeners[event_type]:
                method(event)
                logger.debug(f"Dispatching event {event_type} to method {method.__name__}") if self.debug==True else None
    
    def subscribe(self,event_name:str, method:callable):
        if event_name not in self.listeners:
            self.listeners[event_name] = []

        if method not in self.listeners[event_name]:
            self.listeners[event_name].append(method)
            logger.debug(f"Method {method.__name__} subscribed to event {event_name}")if self.debug==True else None
            
    
    def unsubscribe_all(self):
        self.listeners.clear()
        logger.debug(f"Events list cleared")
        
        
                
    