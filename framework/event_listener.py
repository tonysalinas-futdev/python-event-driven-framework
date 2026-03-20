from typing import Callable

class EventListener():
    def __init__(self, order:int, method:Callable):
        self.method=method
        self.order=order
        