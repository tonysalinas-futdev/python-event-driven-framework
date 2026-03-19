from datetime import datetime
import uuid 


class Event():
    class Event:
        """
    Base class for all events in the framework.

    Every custom event should inherit from this class. It provides two
    automatically generated attributes that uniquely identify and timestamp
    each event instance:

    Attributes:
        id (uuid.UUID): A unique identifier automatically assigned to the event
            when it is created.
        timestamp (datetime.datetime): The exact date and time when the event
            instance was created.

    Usage:
        class UserLoginEvent(Event):
            def __init__(self, username: str):
                super().__init__()
                self.username = username

        # Example instantiation
        login_event = UserLoginEvent("John Doe")
        print(login_event.id)        # Unique UUID
        print(login_event.timestamp) # Creation time
    """
    
    def __init__(self):
        self.id=uuid.uuid4()
        self.timestamp=datetime.now()
    
