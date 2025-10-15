from pydantic import BaseModel
from typing import  Optional


class InvestmentState(BaseModel):
    type: Optional[str] = None
    location: Optional[str] = None
    budget: Optional[float] = None
    action: Optional[str] = None