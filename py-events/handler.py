from publisher import EventPublisher
from typing import Callable,Type,FrozenSet
from event import Event
from subscribers import subscribe_by_class,get_params_from_method,subscribe_by_param_annotation


def event_handler(publisher: EventPublisher,  event_class: Type[Event] | FrozenSet[Event]=None,order:int=None):
    """
    Decorator used to register a function as an event handler.

    This decorator subscribes the decorated function to one or more event classes
    through the provided EventPublisher. It supports two modes of subscription:

    1. Explicit event class subscription:
       - If `event_class` is provided, the function will be subscribed to that
         specific event class (or to each class in the given FrozenSet).
       - The optional `order` parameter defines the execution order of this handler
         relative to other handlers subscribed to the same event.

    2. Parameter annotation-based subscription:
       - If `event_class` is not provided, the decorator inspects the parameter
         annotations of the decorated function.
       - Each annotated parameter that corresponds to an Event type will be used
         to automatically subscribe the function to that event.

    Args:
        publisher (EventPublisher): The event publisher responsible for managing
            subscriptions and dispatching events.
        event_class (Type[Event] | FrozenSet[Type[Event]], optional): The event
            class (or set of event classes) to subscribe the function to. If not
            provided, parameter annotations are used instead.
        order (int, optional): Execution order of the handler among all listeners
            of the same event. Lower values run earlier. Defaults to None.

    Returns:
        Callable: The decorated function, now registered as an event handler.

    Example:
        @event_handler(publisher, UserLoginEvent, order=1)
        def handle_login(event: UserLoginEvent):
            print(f"User {event.username} logged in")

        # Or using parameter annotations:
        @event_handler(publisher)
        def handle_login(event: UserLoginEvent):
            print(f"User {event.username} logged in")
    """
    def wrapper(func:Callable):
        if event_class!=None:
            return subscribe_by_class(event_class,func,publisher,order)
        params = get_params_from_method(func)
        subscribe_by_param_annotation(params,publisher,order,func)
    return wrapper
                    
                