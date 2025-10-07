from src.workflows.modules.appointments.services.calendar.domain.calendar_service import CalendarService
from src.workflows.modules.appointments.services.calendar.infrastructure.google.dependencies import get_google_calendar_service

def get_calendar_service() -> CalendarService:
    return get_google_calendar_service()
