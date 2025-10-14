import os
from fastapi import Depends
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph

from src.shared.domain.models import State

from src.workflows.modules.appointments.graph import create_appointments_graph
from src.workflows.modules.data_collection.agent.agent import DataCollector
from src.workflows.modules.data_collection.agent.dependencies import get_data_collector
from src.workflows.modules.investment_data.agent.agent import InvestmentDataAgent
from src.workflows.modules.investment_data.agent.dependencies  import get_iventstment_data_agent

def create_graph(
    appointments_subgraph: CompiledStateGraph = Depends(create_appointments_graph),
    data_collector: DataCollector = Depends(get_data_collector),
    investment_data_agent: InvestmentDataAgent = Depends(get_iventstment_data_agent)
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
        appointments_state = await appointments_subgraph.ainvoke(state["appointment_data"])

        return {"appointment_data": appointments_state}

    
    async def investment_data_node(state: State):
        await investment_data_agent.interact(
            ws_connection_id=state["call_id"],
            state=state["investment_data"],
            chat_history=state["chat_history"],
            input=state["input"]
        )

        return state
    
    def router(state: State):
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
        router,
        {
            "appointments": "appointments",
            "investment_data": "investment_data"
        }
    )
    graph.add_edge("appointments", END)
    graph.add_edge("investment_data", END)

    return graph.compile()