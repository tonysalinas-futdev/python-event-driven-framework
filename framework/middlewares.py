from event import Event
from singleton.singleton import Singleton
from typing import List,Callable

class EventMiddleware():
    """
    Base class for all middleware components in the event framework.

    Middleware provides a mechanism to intercept, process, or transform
    events before they reach their final handlers. Each middleware can
    optionally define an execution order to control the sequence in which
    multiple middlewares are applied.

    Attributes:
        order (int, optional): Defines the execution order of the middleware.
            Lower values are executed earlier. If None, the middleware is
            placed at the end of the chain.

    Methods:
        process(event: Event, next_middl: Callable):
            Processes the given event. If a next middleware or handler exists,
            it forwards the event to it. Otherwise, it returns the event
            unchanged.
    """
    def __init__(self,order:int=None):
        self.order=order
        
    def process(self, event:Event, next_middl)->Event:
        if next_middl!=None:
            return next_middl(event)
        return event


class MiddlewarePipeline(Singleton):
    def __init__(self):
        self.middlewares:List[EventMiddleware]=[]
    
    def add(self,middl:EventMiddleware)->None:
        if not isinstance(middl,EventMiddleware):
            raise TypeError(f"'{middl.__class__.__name__}' is not a instance of 'EventMiddleware'")
        self.middlewares.append(middl)

    def run_pipeline(self,handler:Callable)->None:
        if len(self.middlewares)==0:
            return
        next_handler=handler
        ordered_middlewares=sorted(self.middlewares,key=lambda o: (o.order is None, o.order))
        for m in reversed(ordered_middlewares):
            current=next_handler
            next_handler=lambda event, m=m, current=current: m.around(event,current)
        return next_handler
