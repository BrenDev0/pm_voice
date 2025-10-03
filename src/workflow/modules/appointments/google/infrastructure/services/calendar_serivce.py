from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

import os
import datetime
from typing import List, Dict
import json

from src.workflow.modules.appointments.google.infrastructure.decorators.errors import google_api_error_handler

class GoogleCalendarService:
    __MODULE = "google.service.calendar_service"
    def __init__(self):
        self.calendar_id = os.getenv("GOOGLE_CALENDAR_ID")


    @staticmethod
    def build_service(credentials: Credentials, version: str = 'v3' ):
        return build(
            serviceName="calendar",
            version=version,
            credentials=credentials
        )
    
    @google_api_error_handler(module=__MODULE)
    def get_events(
        self,
        credentials: Credentials
    ):
        service = self.build_service(
            credentials=credentials
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
    def create_event(
        self,
        credentials: Credentials,
        summary: str,
        start_time: datetime,
        end_time: datetime,
        attendees: List[Dict[str, str]] = None,
    ):
        service = self.build_service(credentials=credentials)
  
        event_data = {
            'summary': summary,
            'start': {
                'dateTime': start_time,
                'timeZone': 'America/Merida',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'America/Merida'
            }
        }

        if attendees:
            event_data["attendees"] = attendees

    
        event = service.events().insert(
            calendarId=self.calendar_id,
            body=event_data
        ).execute()
       
            
            

        return event