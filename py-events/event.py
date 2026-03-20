from datetime import datetime
import uuid 
import attr

@attr.frozen
class Event:
    """
    Immutable base class for all events in the framework.

    Every custom event must inherit from this class. Because the base class
    is decorated with `@attr.frozen`, all subclasses are automatically frozen
    as well. This ensures that event instances cannot be modified after
    creation, preserving consistency and traceability across the system.

    Attributes:
        id (uuid.UUID): A unique identifier automatically generated when
            the event is created.
        timestamp (datetime.datetime): The exact date and time when the
            event instance was created.
        type (str): The name of the event class, useful for distinguishing
            event types during dispatching and logging.

    Usage:
        @attr.frozen
        class UserLoginEvent(Event):
            username: str

        # Example instantiation
        login_event = UserLoginEvent("John Doe")
        print(login_event.id)        # Unique UUID
        print(login_event.timestamp) # Creation time
        print(login_event.type)      # "UserLoginEvent"

    """

    def __init__(self):
        self.id=attr.field(factory=uuid.uuid4)
        self.timestamp=attr.field(factory=datetime.now)
        self.type=attr.field(default=self.__class__.__name__)
    
