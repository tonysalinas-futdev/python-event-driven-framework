from datetime import datetime
import uuid 


class Event():
    def __init__(self):
        self.id=uuid.uuid4()
        self.timestamp=datetime.now()
    
