# File: a2a_handshake/langgraph_greeter/greeter_agent_logic.py

from typing import TypedDict
from langgraph.graph import StateGraph, END


# Define the state of our graph. It's a dictionary with a single 'message' key.
class GreeterState(TypedDict):
    message: str


def greet(state: GreeterState) -> GreeterState:
    """A simple node that returns a friendly greeting."""
    print("LangGraph node 'greet' was executed.")
    return {"message": "Hello from your new friend, the LangGraph agent!"}


# Create the graph, add the single node, and define the entry and exit points.
workflow = StateGraph(GreeterState)
workflow.add_node("greet", greet)
workflow.set_entry_point("greet")
workflow.add_edge("greet", END)

# Compile the graph into a runnable object that we can call later.
langgraph_app = workflow.compile()