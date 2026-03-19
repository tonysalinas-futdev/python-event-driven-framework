import inspect
from publisher import EventPublisher
from typing import Callable,OrderedDict,Type,FrozenSet
from event import Event
from errors.exceptions import InvalidEventTypeError, UnannotatedEventParameterError,EventSubclassRequiredError
from event_listener import EventListener

def verify_event(event_class:Event):
    if not issubclass(event_class,Event):
        raise InvalidEventTypeError(event_class)


def get_params_from_method(func:Callable):
    signature=inspect.signature(func)
    params = signature.parameters
    return params

def validate_parameter_annotation(param:inspect.Parameter):
    if param.annotation is inspect._empty:
        raise UnannotatedEventParameterError(param)
    if not issubclass(param.annotation, Event):
        raise EventSubclassRequiredError(param)
    return param


def subscribe_by_param_annotation(params:OrderedDict,publisher:EventPublisher,order:int,method:Callable):
    for param in params.values():
        validate_parameter_annotation(param)
        publisher.subscribe(param.annotation, EventListener(order if order!=None else None,method))
        


def subscribe_by_class(class_:Type[Event] | FrozenSet[Type[Event]],method:Callable,publisher:EventPublisher, order:int=None):
    if isinstance(class_, FrozenSet):
        for e in class_:
            verify_event(e)
            publisher.subscribe(e,EventListener(order,method))
    elif issubclass(class_,Event):
        publisher.subscribe(class_,EventListener(order,method))

    else:
        raise InvalidEventTypeError(class_)
        
        
                    
                
