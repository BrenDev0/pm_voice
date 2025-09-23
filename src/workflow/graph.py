from fastapi import Depends
from langgraph.graph import StateGraph, START, END

from src.workflow.state import State
from src.dependencies.agents import get_orchestrator_agent
from src.workflow.agents.orchestrator.orchestrator_agent import Orchestrator



def create_graph(
    orchestrator: Orchestrator = Depends(get_orchestrator_agent)
):
    graph = StateGraph(State)

    async def orchestrator_node(state: State):
        response = await orchestrator.interact(state=state)

        return {"response": response}

    graph.add_node("orchestrator", orchestrator_node)

    graph.add_edge(START, "orchestrator")
    graph.add_edge("orchestrator", END)

    return graph.compile()