from langgraph.graph import  StateGraph, START, END
from  fastapi import Depends

from src.workflows.modules.appointments.agent import ApointmentsAgent
from src.workflows.modules.appointments.models import AppointmentState
from src.workflows.modules.appointments.dependencies import get_appoinments_agent

from src.workflows.modules.appointments.services.calendar.domain.calendar_service import CalendarService
from src.workflows.modules.appointments.services.calendar.infrastructure.google.dependencies import get_google_calendar_service

def create_appointments_graph(
    appoinment_agent: ApointmentsAgent = Depends(get_appoinments_agent),
    calendar_service: CalendarService = Depends(get_google_calendar_service)
):
    graph = StateGraph(AppointmentState)

    def router(state: AppointmentState):
        if state.appointment_datetime:
            return "check_availability"
        else: 
            return "get_datetime"

    async def get_datetime_node(state: AppointmentState):
        response = await appoinment_agent.interact()

        return {"appointment_datetime": response}

    async def check_availability_node(state: AppointmentState) -> bool:
        pass

    async def unavailable_node(state: AppointmentState):
        pass

    async def confirmation_node(state: AppointmentState):
        pass

   
    graph.add_node("get_datetime", get_datetime_node)
    graph.add_node("check_availability", check_availability_node)
    graph.add_node("unavailable", unavailable_node)
    graph.add_node("confirmation", confirmation_node)

    graph.add_conditional_edges(
        START,
        router,
        {
            "get_datetime": "get_datetime",
            "check_availability": "check_availability"
        }
    )

    graph.add_conditional_edges(
        "check_availability",
        {
            True: "confirmation",
            False: "unavailable"
        }
    )

    graph.add_edge("confirmation", END)



    return graph.compile()
