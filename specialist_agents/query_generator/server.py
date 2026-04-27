# File: specialist_agents/query_generator/server.py
import uuid
from typing import TypedDict
from dotenv import load_dotenv

from langgraph.graph import StateGraph, END

from a2a.types import (
    AgentCard, AgentSkill, AgentCapabilities, Part, TextPart,
)
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.tasks import TaskUpdater, InMemoryTaskStore
from a2a.server.events import EventQueue
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
import uvicorn

load_dotenv()


# === LangGraph workflow ===
class QueryState(TypedDict):
    user_topic: str
    queries: list[str]


def generate_queries(state: QueryState) -> QueryState:
    """Generate 3 search queries from a user topic."""
    topic = state["user_topic"]
    queries = [
    f"What is {topic}?",
    f"Recent news about {topic}",
      ]
    print(f"Generated queries for '{topic}': {queries}")
    return {"user_topic": topic, "queries": queries}


workflow = StateGraph(QueryState)
workflow.add_node("generate", generate_queries)
workflow.set_entry_point("generate")
workflow.add_edge("generate", END)
query_app = workflow.compile()


# === A2A AgentCard ===
agent_card = AgentCard(
    name="Query Generator",
    description="Generates search queries from a topic.",
    url="http://localhost:10002/",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=True),
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
    skills=[
        AgentSkill(
            id="generate_queries",
            name="Generate Search Queries",
            description="Creates 3 search queries from a topic.",
            tags=["research", "queries"],
            examples=["AI in healthcare", "climate change"],
        )
    ],
)


# === AgentExecutor ===
class QueryGeneratorExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue):
        topic = context.get_user_input()
        print(f"Received topic: '{topic}'")

        updater = TaskUpdater(event_queue, context.task_id, context.context_id)

        result = await query_app.ainvoke(
            {"user_topic": topic, "queries": []},
            {"configurable": {"thread_id": context.context_id}},
        )

        queries_text = "\n".join(f"- {q}" for q in result["queries"])

        await updater.add_artifact(
            [Part(root=TextPart(text=queries_text))],
            name="search_queries",
        )
        await updater.complete()

    async def cancel(self, context, event_queue):
        raise NotImplementedError()


if __name__ == "__main__":
    handler = DefaultRequestHandler(
        agent_executor=QueryGeneratorExecutor(),
        task_store=InMemoryTaskStore(),
    )
    app = A2AStarletteApplication(agent_card=agent_card, http_handler=handler)
    print("Starting LangGraph Query Generator on http://localhost:10002...")
    uvicorn.run(app.build(), host="0.0.0.0", port=10002)