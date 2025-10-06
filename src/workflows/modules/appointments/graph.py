from langgraph.graph import  StateGraph, START, END
from  fastapi import Depends

from src.workflows.modules.appointments.infrastructure.agent import ApointmentsAgent
from src.workflows.modules.appointments.models import AppointmentData
from src.workflows.modules.appointments.infrastructure.dependencies import get_appoinments_agent

def create_appointments_graph(
    appoinment_agent: ApointmentsAgent = Depends(get_appoinments_agent)
):
    graph = StateGraph(AppointmentData)

    def router(state: AppointmentData):
        if state.appointment_datetime:
            return "check_availability"
        else: 
            return "get_datetime"

    async def get_datetime_node(state: AppointmentData):
        response = await appoinment_agent.interact()

        return {"appointment_datetime": response}

    async def check_availability_node(state: AppointmentData) -> bool:
        pass

    async def unavailable_node(state: AppointmentData):
        pass

    async def confirmation_node(state: AppointmentData):
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
