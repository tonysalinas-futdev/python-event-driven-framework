import inspect
from publisher import EventPublisher
from typing import Callable,OrderedDict
from event import Event
from errors.exceptions import InvalidEventTypeError, UnannotatedEventParameterError,EventSubclassRequiredError

def verify_event(event_class):
    if not issubclass(event_class,Event):
        raise InvalidEventTypeError(event_class)
    return event_class

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

def subscribe_by_param_annotation(params:OrderedDict,publisher:EventPublisher,func:Callable):
    for param in params.values():
        validate_parameter_annotation(param)
        publisher.subscribe(param.annotation.__name__, func)
        
        
        
    

def event_handler(publisher: EventPublisher):
    def wrapper(func:Callable):
        params = get_params_from_method(func)
        subscribe_by_param_annotation(params,publisher,func)
    return wrapper
                    
                
