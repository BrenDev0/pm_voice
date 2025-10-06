from dotenv import load_dotenv
load_dotenv()
import pytest
import datetime

from src.core.dependencies.configure_container import configure_container

from src.workflows.modules.appointments.google.infrastructure.services.service import GoogleService
from src.workflows.modules.appointments.google.infrastructure.services.calendar_serivce import GoogleCalendarService
from src.workflows.modules.appointments.google.infrastructure.services.client_manager import GoogleClientManager


configure_container()
google_service = GoogleService(
    client_manager=GoogleClientManager(),
    calendar_service=GoogleCalendarService()
)

# @pytest.mark.asyncio
# async def test_get_events():
#     creds = await google_service.client_manager.get_credentialed_client()
#     events = google_service.calendar_service.get_events(credentials=creds)

#     print(events)

#     assert events == None


@pytest.mark.asyncio
async def test_create_event():
    summary = "testing event"
    start_time = datetime.datetime(year=2025, month=10, day=3, hour=15).isoformat()
    end_time = datetime.datetime(year=2025, month=10, day=3, hour=15, minute=30).isoformat()
    attendees = ["lahey1991@gmail.com"]

    print(start_time)
    print(end_time)

    creds = await google_service.client_manager.get_credentialed_client()
    event = google_service.calendar_service.create_event(
        credentials=creds,
        summary=summary,
        start_time=start_time,
        end_time=end_time,
        attendees=attendees
    )

    assert event 