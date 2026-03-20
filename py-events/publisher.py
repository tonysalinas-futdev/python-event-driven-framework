from singleton.singleton import Singleton
from event import Event
from typing import Dict,Type, List,Callable
from event_listener import EventListener
from errors.exceptions import MissingEventError
from middlewares import MiddlewarePipeline



pipelin=MiddlewarePipeline()

class EventPublisher(Singleton):
    """
    Central event dispatcher and subscription manager.

    The EventPublisher is responsible for managing event listeners and
    dispatching events to their corresponding handlers. It follows the
    Singleton pattern to ensure a single publisher instance across the
    application.

    Attributes:
        listeners (Dict[Type[Event], List[EventListener]]): A mapping of event
            classes to their subscribed listeners.
        debug (bool): Flag to enable or disable debug logging.
        in_order (bool): Flag indicating whether listeners should be executed
            in a defined order.

    Methods:
        publish(event: Event):
            Dispatches the given event to all subscribed listeners. If
            `in_order` is True, listeners are sorted by their `order`
            attribute before execution. Raises MissingEventError if no
            listeners are registered for the event type.

        subscribe(event_class: Type[Event], event_listener: EventListener):
            Subscribes a listener to the specified event class. If the event
            class has no listeners yet, it initializes the list. Logs the
            subscription if debug mode is enabled.

        unsubscribe(event: Type[Event], listener_method: Callable):
            Removes a listener method from the specified event class. Logs the
            removal if debug mode is enabled.

        unsubscribe_all():
            Clears all registered listeners across all event classes. Logs the
            reset if debug mode is enabled.

    Example:
        publisher = EventPublisher(debug=True, in_order=True)

        # Subscribe a handler
        publisher.subscribe(UserLoginEvent, EventListener(order=1, method=handle_login))

        # Publish an event
        publisher.publish(UserLoginEvent(username="Tony"))

        # Unsubscribe a handler
        publisher.unsubscribe(UserLoginEvent, handle_login)

        # Clear all listeners
        publisher.unsubscribe_all()
    """
    def __init__(self,debug:bool=False, in_order:bool=False):
        self.listeners:Dict[Event,List[EventListener]]={}
        self.debug=debug
        self.in_order=in_order
        
    def publish(self,event:Event):
        event_type=event.__class__
        if event_type not in self.listeners:
            raise MissingEventError(event_type.__name__)
        if self.in_order==True:
            self.listeners[event_type].sort(key=lambda o: (o.order is None, o.order))

        def dispatch(ev:Event):
            for listener in self.listeners[event_type]:
                listener.method(ev)
        pipeline=pipelin.run_pipeline(dispatch)
        pipeline(event)
    
    def subscribe(self,event_class:Type[Event], event_listener:EventListener):
        if event_class not in self.listeners:
            self.listeners[event_class] = []

        if event_listener not in self.listeners[event_class]:
            self.listeners[event_class].append(event_listener)

            

    def unsubscribe(self, event:Type[Event], listener_method:Callable):
        for e in self.listeners[event]:
            if e.method==listener_method:
                self.listeners[event].remove(e)

    
    
    def unsubscribe_all(self):
        self.listeners.clear()



    