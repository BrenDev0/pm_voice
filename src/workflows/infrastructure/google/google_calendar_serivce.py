import os
import datetime

from src.workflows.domain.entities import Event
from src.workflows.domain.services.calendar_service import CalendarService
from src.workflows.infrastructure.google.errors_decorator import google_api_error_handler
from src.workflows.infrastructure.google.google_client_manager import GoogleClientManager


class GoogleCalendarService(CalendarService):
    __MODULE = "google.service.calendar_service"
    def __init__(
        self
    ):
        self.calendar_id = os.getenv("GOOGLE_CALENDAR_ID")
        self.__service_key = "calendar"


    @google_api_error_handler(module=__MODULE)
    async def get_events(
        self,
    ):
        service = await GoogleClientManager.build_service(
            service_key=self.__service_key
        )

        now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()

        results = (
            service.events()
            .list(
                calendarId=self.calendar_id,
                timeMin=now,
                singleEvents=True,
                orderBy="startTime"
            )
            .execute()
        )

        events = results.get("items", [])

        if not events:
            return None
        
        return events
    
    @google_api_error_handler(module=__MODULE)
    async def create_event(
        self,
        event: Event
    ):
        service =  await GoogleClientManager.build_service(service_name=self.__service_key)
  
        event_data = {
            'summary': event.title,
            'start': {
                'dateTime': event.start,
                'timeZone': 'America/Merida',
            },
            'end': {
                'dateTime': event.end,
                'timeZone': 'America/Merida'
            }
        }

        if event.attendees:
            event_data["attendees"] = event.attendees

    
        event = service.events().insert(
            calendarId=self.calendar_id,
            body=event_data
        ).execute()
       
        return event
    
    @google_api_error_handler(module=__MODULE)
    async def check_availability(
        self,    
        appointment_datetime: str
    ):
       
        service =  await GoogleClientManager.build_service(service_name=self.__service_key)
       

        body = {
            "timeMin": "2025-10-17T18:00:00-06:00",
            "timeMax": "2025-10-17T18:30:00-06:00",
            "timeZone": "America/Merida",
            "items": [{"id": self.calendar_id}]
        }

        
        res = service.freebusy().query(body=body).execute()
        print(res, "RESSSSSSSSSSSSSSSSSS")
       
        # calendars = res.get("calendars", {})
        # busy_slots = calendars.get(self.calendar_id, {}).get("busy", [])

        # return len(busy_slots) == 0