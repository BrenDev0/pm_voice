from src.workflows.modules.appointments.domain.calendar_service import CalendarService
from src.workflows.modules.appointments.infrastructure.google.services.google_calendar_serivce import GoogleCalendarService

def get_calendar_service() -> CalendarService:
    return GoogleCalendarService()
