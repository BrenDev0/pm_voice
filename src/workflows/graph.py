import os
from fastapi import Depends
from langgraph.graph import StateGraph, START, END

from src.shared.domain.models import State
from src.workflows.modules.appointments.application.agent import AppointmentsAgent
from src.workflows.modules.appointments.dependencies import get_appoinments_agent
from src.workflows.modules.data_collection.application.agent import DataCollector
from src.workflows.modules.data_collection.dependencies import get_data_collector
from src.workflows.modules.investment_data.application.agent import InvestmentDataAgent
from src.workflows.modules.investment_data.dependencies  import get_iventstment_data_agent

def create_graph(
    appointments_agent: AppointmentsAgent  = Depends(get_appoinments_agent),
    data_collector: DataCollector = Depends(get_data_collector),
    investment_agent: InvestmentDataAgent = Depends(get_iventstment_data_agent)
 ):
    graph = StateGraph(State)

    async def data_collection_node(state: State):
        response = await data_collector.interact(state=state)

        return {
            "investment_data": response.investment_data,
            "appointment_data": response.appointment_data,
            "client_intent": response.client_intent
        }
    
    async def appointments_node(state: State):
        appointments_state = state["appointment_data"]

     
        res = await appointments_agent.interact(
            ws_connection_id=state["call_id"],
            state=appointments_state,
            chat_history=state["chat_history"],
            input=state["input"]
        )

        return {"appointments_state": res}


    async def investment_data_node(state: State):
        await investment_agent.interact(
            ws_connection_id=state["call_id"],
            state=state["investment_data"],
            chat_history=state["chat_history"],
            input=state["input"]
        )

        return state
    
    def intent_router(state: State):
        intent = state["client_intent"]
        
        if intent == "investment":
            return "investment_data"
        
        elif intent == "appointments":
            return "appointments"
        
        else:
            return "confirmation"
    
    graph.add_node("data_collection", data_collection_node)
    graph.add_node("appointments", appointments_node)
    graph.add_node("investment_data", investment_data_node)

    graph.add_edge(START, "data_collection")
    graph.add_conditional_edges(
        "data_collection",
        intent_router,
        {
            "appointments": "appointments",
            "investment_data": "investment_data"
        }
    )
    graph.add_edge("appointments", END)
    graph.add_edge("investment_data", END)

    return graph.compile()