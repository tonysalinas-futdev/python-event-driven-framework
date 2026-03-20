
# Event Framework

A lightweight event-driven framework in Python that allows you to define events, subscribe handlers, and publish them through a central publisher.  
It is designed with clarity, maintainability, and extensibility in mind.

---

## 📂 Project Structure

- `event.py` → Defines the base `Event` class, from which all custom events must inherit.
- `publisher.py` → Contains the `EventPublisher` class, the central dispatcher and subscription manager.
- `handler.py` → Provides the `event_handler` decorator to register event handlers.
- `middlewares.py` → Defines the base class `EventMiddleware` for creating custom middleware, and the `MiddlewarePipeline` for registering and executing all middleware components.

## ⚙️ Components

### 1. `Event` (event.py)

```python
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
```

**Usage Example:**
```python
      @attr.frozen
        class UserLoginEvent(Event):
            username: str
                    # Example instantiation
        login_event = UserLoginEvent("John Doe")
        print(login_event.id)        # Unique UUID
        print(login_event.timestamp) # Creation time
        print(login_event.type)      # "UserLoginEvent"
```

---

### 2. `EventPublisher` (publisher.py)

```python
class EventPublisher(Singleton):
    """
    Central event dispatcher and subscription manager.

    The EventPublisher manages event listeners and dispatches events to their
    corresponding handlers. It ensures a single publisher instance across the
    application.

    Methods:
        publish(event: Event): Dispatches an event to all subscribed listeners.
        subscribe(event_class: Type[Event], event_listener: EventListener):
            Subscribes a listener to an event class.
        unsubscribe(event: Type[Event], listener_method: Callable):
            Removes a listener method from an event class.
        unsubscribe_all(): Clears all registered listeners.
    """
```

**Usage Example:**
```python
publisher = EventPublisher(debug=True, in_order=True)

# Subscribe a handler
publisher.subscribe(UserLoginEvent, EventListener(order=1, method=handle_login))

# Publish an event
publisher.publish(UserLoginEvent(username="Tony"))

# Unsubscribe a handler
publisher.unsubscribe(UserLoginEvent, handle_login)

# Clear all listeners
publisher.unsubscribe_all()
```

---

### 3. `event_handler` Decorator (handler.py)

```python
def event_handler(
    publisher: EventPublisher,
    event_class: Type[Event] | FrozenSet[Event] = None,
    order: int = None
):
    """
    Decorator used to register a function as an event handler.

    Supports two modes:
    1. Explicit subscription: Provide `event_class` to subscribe directly.
    2. Annotation-based subscription: If `event_class` is not provided,
       parameter annotations of the function are inspected to determine
       which events to subscribe to.
    """
```

**Usage Example:**
```python
@event_handler(publisher, UserLoginEvent, order=1)
def handle_login(event: UserLoginEvent):
    print(f"User {event.username} logged in")

# Or using parameter annotations:
@event_handler(publisher)
def handle_login(event: UserLoginEvent):
    print(f"User {event.username} logged in")
```

### Example: Using EventMiddleware

```python
from event import Event
from middlewares import EventMiddleware, MiddlewarePipeline

class UserLoginEvent(Event):
    def __init__(self, username: str):
        super().__init__()
        self.username = username

class LoggingMiddleware(EventMiddleware):
    def process(self, event, next_middl):
        print(f"[Start] {event.type}")
        result = next_middl(event)
        print(f"[End] {event.type}")
        return result

pipeline = MiddlewarePipeline()
pipeline.add(LoggingMiddleware(order=1))

def handle_login(event: UserLoginEvent):
    print(f"Handling login for {event.username}")

handler = pipeline.run_pipeline(handle_login)
handler(UserLoginEvent("Tony"))
```

---

## 🚀 Getting Started

1. Define your custom events by inheriting from `Event`.
2. Create an `EventPublisher` instance.
3. Use the `event_handler` decorator or `subscribe` method to register handlers.
4. Publish events with `publisher.publish(event)`.

---

## 🧩 Example Workflow

```python
# event.py
      @attr.frozen
        class UserLoginEvent(Event):
            username: str

# handler.py
@event_handler(publisher, UserLoginEvent, order=1)
def handle_login(event: UserLoginEvent):
    print(f"User {event.username} logged in")

# main.py
publisher.publish(UserLoginEvent(username="Tony"))
```

---

## 📖 Notes

- `EventPublisher` is a **Singleton**, ensuring only one dispatcher exists.
- Handlers can be executed in order if `in_order=True`.
- Debug logging can be enabled with `debug=True`.

---

## ✅ Conclusion

This framework provides a simple yet powerful way to implement event-driven programming in Python.  
It is extensible, easy to maintain, and supports both explicit and annotation-based handler registration.

