import os
from fastapi import Depends
from langgraph.graph import StateGraph, START, END

from src.workflow.state import State

from src.workflow.modules.data_collection.agent import DataCollector
from src.workflow.modules.data_collection.dependencies import get_data_collector

from src.workflow.base_agent import BaseAgent

from src.workflow.modules.client_data.dependencies import get_client_data_agent
from src.workflow.modules.investment_data.dependencies  import get_iventstment_data_agent

def create_graph(
    data_collector: DataCollector = Depends(get_data_collector),
    client_data_agent: BaseAgent  = Depends(get_client_data_agent),
    investment_data_agent: BaseAgent = Depends(get_iventstment_data_agent)
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
        pass

    async def client_data_node(state: State):
        await client_data_agent.interact(state=state)
        return state
    
    async def investment_data_node(state: State):
        await investment_data_agent.interact(state=state)
    
    def router(state: State):
        pass
    
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