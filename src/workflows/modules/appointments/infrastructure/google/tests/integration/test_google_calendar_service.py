from dotenv import load_dotenv
load_dotenv()
import pytest
import datetime

from src.shared.dependencies.configure_container import configure_container

from src.workflows.modules.appointments.services.calendar.infrastructure.google.services.google_calendar_serivce import GoogleCalendarService
from src.workflows.modules.appointments.services.calendar.infrastructure.google.services.client_manager import GoogleClientManager
from src.workflows.modules.appointments.services.calendar.domain.entities import Event


configure_container()
google_calendar_service = GoogleCalendarService(
    client_manager=GoogleClientManager()
)

# @pytest.mark.asyncio
# async def test_get_events():
#     creds = await google_service.client_manager.get_credentialed_client()
#     events = google_service.calendar_service.get_events(credentials=creds)

#     print(events)

#     assert events == None


@pytest.mark.asyncio
async def test_create_event():
    event_data = Event(
        title="testing event",
        start=datetime.datetime(year=2025, month=10, day=3, hour=15).isoformat(),
        end=datetime.datetime(year=2025, month=10, day=3, hour=15, minute=30).isoformat(),
        attendees=["lahey1991@gmail.com"]
    )
    
    event = google_calendar_service.create_event(
        event=event_data
    )

    assert event 