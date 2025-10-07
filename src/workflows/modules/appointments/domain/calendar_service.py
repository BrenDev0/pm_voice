from abc import ABC, abstractmethod
from src.workflows.modules.appointments.domain.entities import Event
from typing import List

class CalendarService(ABC):
    @classmethod
    def get_events():
        raise NotImplementedError
    
    def add_event(event: Event):
        raise NotImplementedError