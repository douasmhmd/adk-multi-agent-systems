# File: a2a_handshake/langgraph_greeter/server.py
from a2a.types import (
    AgentCard,
    AgentSkill,
    AgentCapabilities,
    Part,
    TextPart,
)
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.tasks import TaskUpdater, InMemoryTaskStore
from a2a.server.events import EventQueue
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
import uvicorn

from greeter_agent_logic import langgraph_app


# === Agent Card: public description ===
greeter_agent_card = AgentCard(
    name="LangGraph Greeter",
    description="A friendly agent built with LangGraph that offers a greeting.",
    url="http://localhost:10000/",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=True),
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
    skills=[
        AgentSkill(
            id="greet",
            name="Simple Greeting",
            description="Returns a friendly greeting.",
            tags=["greeting"],
            examples=["Hello", "Hi there!"],
        )
    ],
)


# === AgentExecutor: bridge between A2A and LangGraph ===
class GreeterAgentExecutor(AgentExecutor):
    """An AgentExecutor that wraps our simple LangGraph agent."""

    async def execute(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        print(f"Greeter Agent received request: '{context.get_user_input()}'")

        updater = TaskUpdater(event_queue, context.task_id, context.context_id)

        final_state = await langgraph_app.ainvoke(
            {}, {"configurable": {"thread_id": context.context_id}}
        )

        response_text = final_state.get(
            "message", "Error: No message from graph."
        )

        await updater.add_artifact(
            [Part(root=TextPart(text=response_text))],
            name="greeting_response",
        )
        await updater.complete()

    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise NotImplementedError("Cancellation is not supported.")


# === Server bootstrap ===
if __name__ == "__main__":
    request_handler = DefaultRequestHandler(
        agent_executor=GreeterAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    server_app = A2AStarletteApplication(
        agent_card=greeter_agent_card,
        http_handler=request_handler,
    )

    print("Starting LangGraph Greeter Agent on http://localhost:10000...")
    uvicorn.run(server_app.build(), host="0.0.0.0", port=10000)