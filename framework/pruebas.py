from publisher import EventPublisher
from handler import event_handler
from event import Event

publisher_instance=EventPublisher(debug=True, in_order=True)

class LoginIntentEvent(Event):
    def __init__(self, email,name):
        super().__init__()
        self.email=email
        self.name=name
        

class UserInBdEvent(Event):
    def __init__(self, email,name):
        super().__init__()
        self.email=email
        self.name=name


class AnotherEvent(Event):
    def __init__(self, email,name):
        super().__init__()
        self.email=email
        self.name=name


def publish_login_event(event:LoginIntentEvent):
    publisher_instance.publish(event)

@event_handler(publisher=publisher_instance, event_class=LoginIntentEvent)    
def handleUserLoginEvent(event: LoginIntentEvent):

    print(f"El usuario {event.name} se encuentra en la base de datos")

 
    publisher_instance.publish(UserInBdEvent(event.email,event.name))
    

@event_handler(publisher=publisher_instance, order=1)    
def handleUserLoginEvent2(event: LoginIntentEvent):
    print(f"Se ha loggeado el inicio de sesión del usuario {event.name} ")
    
    publisher_instance.publish(UserInBdEvent(event.email,event.name))
    
@event_handler(publisher=publisher_instance)
def handleUserInDbEvent(event:UserInBdEvent):
    print(f"Se ha creado la cuenta para el usuario {event.name}")
    

event=LoginIntentEvent("tony@gmail.com","Tony")
publish_login_event(event)
print(publisher_instance.listeners)
publisher_instance.unsubscribe_all()
print(publisher_instance.listeners)
publisher_instance.unsubscribe(UserInBdEvent,handleUserInDbEvent)