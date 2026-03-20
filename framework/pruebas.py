from publisher import EventPublisher,pipelin
from handler import event_handler
from event import Event
from middlewares import EventMiddleware
import attr
publisher_instance=EventPublisher(debug=True, in_order=True)

@attr.frozen
class LoginIntentEvent(Event):
    email:str
    name:str
        
@attr.frozen
class UserInBdEvent(Event):
    email:str
    name:str

@attr.frozen
class CredencialesCorrectasEvent(Event):
    email:str
    name:str

class PrintMiddleware(EventMiddleware):
    def __init__(self, order = 2):
        super().__init__(order)
    
    def around(self, event:LoginIntentEvent, next_middl):
            print(f"Logueando el evento {event.__class__.__name__}")
            result=next_middl(event)
            print(f"Se completoel evento {event.__class__.__name__}")
            return result


class SaludoMiddleware(EventMiddleware):
    def __init__(self, order = 1):
        super().__init__(order)
    
    def around(self, event:LoginIntentEvent, next_middl):
            print(f"Holaaaa {event.__class__.__name__}")
            result=next_middl(event)
            return result
        
                
def publish_login_event(event:LoginIntentEvent):
    publisher_instance.publish(event)

@event_handler(publisher=publisher_instance, event_class=LoginIntentEvent)    
def handleUserLoginEvent(event: LoginIntentEvent):
    print(f"El usuario {event.name} está intentando iniciar sesión")
    publisher_instance.publish(CredencialesCorrectasEvent(event.email,event.name))


    

@event_handler(publisher=publisher_instance, order=1)    
def handleCredencialesCorrectasEvent(event: CredencialesCorrectasEvent):
    print(f"El usuario{event.name} tiene las credenciales correctas")
    publisher_instance.publish(UserInBdEvent(event.email,event.name))
    
@event_handler(publisher=publisher_instance)
def handleUserInDbEvent(event:UserInBdEvent):
    print(f"Se ha guardado en la base de datos al usuario {event.name}")

login=PrintMiddleware()
saludo=SaludoMiddleware()
pipelin.add(login)
pipelin.add(saludo)
event=LoginIntentEvent("tony@gmail.com","Tony")
publish_login_event(event)
