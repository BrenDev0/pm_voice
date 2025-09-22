from typing_extensions import TypedDict

class State(TypedDict):
    name: str
    phone: str
    email: str
    investment_type: str
    investment_location: str
    budget: float


