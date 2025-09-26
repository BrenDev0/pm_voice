from typing_extensions import TypedDict
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum

class PropertyType(str, Enum):
    HOUSE = "house"
    APARTMENT = "apartment"
    COMMERCIAL = "commercial"
    LAND = "land"

class PropertyAction(str, Enum):
    BUY = "buy"
    SELL = "sell"
    RENT = "rent"

class InvestmentData(BaseModel):
    type: Optional[PropertyType] = None
    location: Optional[str] = None
    budget: Optional[float] = None
    action: Optional[PropertyAction] = None

class ClientData(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class AppointmentData(BaseModel):
    appointment_datetime: Optional[datetime] = None 

class State(TypedDict):
    call_id: str
    input: str
    chat_history: List[Dict[str, Any]]
    summary: str
    investment_data: InvestmentData
    client_data: ClientData
    appointment_data: AppointmentData


