import inspect
class BasicException(Exception):
    def __init__(self, message:str):
        super().__init__(message)
        
class InvalidEventTypeError(BasicException):
    def __init__(self,event_class):
        self.message=f"The class '{event_class}' is not a subtype of 'Event'"
        super().__init__(self.message)
        
class UnannotatedEventParameterError(BaseException):
    def __init__(self, param:inspect.Parameter):
        self.message=f"The parameter '{param.name}' has no annotation"
        super().__init__(self.message)

class EventSubclassRequiredError(BaseException):
    def __init__(self, param:inspect.Parameter):
        self.message=f"The parameter '{param.name}' is not a subclass of 'Event'"
        super().__init__(self.message)
