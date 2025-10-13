import os
from fastapi import Depends
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph

from src.workflows.models import State

from src.workflows.modules.appointments.graph import create_appointments_graph
from src.workflows.modules.data_collection.agent.agent import DataCollector
from src.workflows.modules.data_collection.agent.dependencies import get_data_collector
from src.workflows.modules.client_data.agent.agent import ClientDataAgent
from src.workflows.modules.client_data.agent.dependencies import get_client_data_agent
from src.workflows.modules.investment_data.agent.agent import InvestmentDataAgent
from src.workflows.modules.investment_data.agent.dependencies  import get_iventstment_data_agent

def create_graph(
    appointments_subgraph: CompiledStateGraph = Depends(create_appointments_graph),
    client_data_agent: ClientDataAgent  = Depends(get_client_data_agent),
    data_collector: DataCollector = Depends(get_data_collector),
    investment_data_agent: InvestmentDataAgent = Depends(get_iventstment_data_agent)
 ):
    graph = StateGraph(State)
    
    async def data_collection_node(state: State):
        response = await data_collector.interact(state=state)

        return {
            "investment_data": response.investment_data,
            "client_data": response.client_data,
            "appointment_data": response.appointment_data
        }
    
    async def appointments_node(state: State):
        appointments_state = await appointments_subgraph.ainvoke(state["appointment_data"])

        return {"appointment_data": appointments_state}

    async def client_data_node(state: State):
        await client_data_agent.interact(
            ws_connection_id=1,
            state=state["client_data"],
            chat_history=state["chat_history"]
        )
        return state
    
    async def investment_data_node(state: State):
        await investment_data_agent.interact(
            state=state["investment_data"],
            chat_history=state["chat_history"]
        )

        return state
    
    def router(state: State):
        print(state, "RESSSSS  STATE")
        client_data = state["client_data"].model_dump()
        investment_data = state["investment_data"].model_dump()
        apppointment_data = state["appointment_data"].model_dump()

        if any(value is None for value in client_data.values()):
            return "client_data"
        
        elif any(value is None for value in investment_data.values()):
            return "investment_data"
        
        elif any(value is None for value in apppointment_data.values()):
            return "appointments"
        
        else:
            return "confirmation"
    
    graph.add_node("data_collection", data_collection_node)
    graph.add_node("appointments", appointments_node)
    graph.add_node("client_data", client_data_node)
    graph.add_node("investment_data", investment_data_node)

    graph.add_edge(START, "data_collection")
    graph.add_conditional_edges(
        "data_collection",
        router,
        {
            "appointments": "appointments",
            "client_data": "client_data",
            "investment_data": "investment_data"
        }
    )
    graph.add_edge("appointments", END)
    graph.add_edge("client_data", END)
    graph.add_edge("investment_data", END)

    return graph.compile()