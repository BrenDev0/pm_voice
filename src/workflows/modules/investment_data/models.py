from pydantic import BaseModel
from typing import  Optional
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

class InvestmentState(BaseModel):
    type: Optional[PropertyType] = None
    location: Optional[str] = None
    budget: Optional[float] = None
    action: Optional[PropertyAction] = None