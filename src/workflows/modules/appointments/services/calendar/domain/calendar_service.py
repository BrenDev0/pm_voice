from abc import ABC, abstractmethod
from src.workflows.modules.appointments.domain.models import EventData
from typing import List

class CalendarService(ABC):
    @classmethod
    def get_events() -> List[EventData]:
        raise NotImplementedError
    
    def add_event(event: EventData):
        raise NotImplementedError