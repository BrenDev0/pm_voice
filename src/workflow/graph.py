import os
from fastapi import Depends
from langgraph.graph import StateGraph, START, END

from src.workflow.state import State
from src.dependencies.agents import get_data_collector
from workflow.agents.data_collection.data_collector import DataCollector



def create_graph(
    data_collector: DataCollector = Depends(get_data_collector)
):
    graph = StateGraph(State)
    
    async def intro_node(state: State):
        pass
    
    async def data_collection_node(state: State):
        await data_collector.interact(state=state)

        return state
    

    graph.add_node("intro", intro_node)
    graph.add_node("data_collection", data_collection_node)

    return graph.compile()