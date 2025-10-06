from fastapi import Depends

from src.workflows.modules.appointments.services.calendar.domain.calendar_service import CalendarService
from workflows.modules.appointments.services.calendar.infrastructure.google.services.google_calendar_serivce import GoogleCalendarService
from src.workflows.modules.appointments.services.calendar.infrastructure.google.services.client_manager import GoogleClientManager


def get_google_calendar_service() -> CalendarService:
    return GoogleCalendarService(
        client_manager=Depends(get_client_manager)
    )

def get_client_manager() -> GoogleClientManager:
    return GoogleClientManager()

