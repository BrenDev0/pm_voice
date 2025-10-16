from abc import ABC, abstractmethod
from src.workflows.domain.entities import Event
from datetime import datetime

class CalendarService(ABC):
    @abstractmethod
    def get_events():
        raise NotImplementedError
    
    @abstractmethod
    def create_event(event: Event):
        raise NotImplementedError
    
    @abstractmethod
    def check_availability(appointment_datetime: datetime):
        raise NotImplementedError
