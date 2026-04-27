# File: a2a_math_agent/server.py
from a2a.types import AgentCard, AgentSkill, AgentCapabilities
from dotenv import load_dotenv
load_dotenv()

math_agent_card = AgentCard(
    name="ADK Math Agent",
    description="A powerful calculator agent from Chapter 6, now A2A-enabled.",
    url="http://localhost:10001/",
    version="2.0-a2a",
    capabilities=AgentCapabilities(streaming=True),
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
    skills=[
        AgentSkill(
            id="add",
            name="Addition",
            description="Adds a list of integers together.",
            tags=["math", "addition"],
        ),
        AgentSkill(
            id="subtract",
            name="Subtraction",
            description="Subtracts one number from another.",
            tags=["math", "subtraction"],
        ),
        AgentSkill(
            id="multiply",
            name="Multiplication",
            description="Multiplies a list of integers.",
            tags=["math", "multiplication"],
        ),
        AgentSkill(
            id="divide",
            name="Division",
            description="Divides one number by another.",
            tags=["math", "division"],
        ),
    ],
)
# === AgentExecutor: bridge between A2A and ADK ===
import uuid
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.tasks import TaskUpdater, InMemoryTaskStore
from a2a.server.events import EventQueue
from a2a.types import Part, TextPart
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from math_agent_ch6.agent import root_agent as math_agent


class MathAgentExecutor(AgentExecutor):
    """An AgentExecutor that runs the existing ADK Math Agent."""

    def __init__(self):
        self._session_service = InMemorySessionService()
        self._runner = Runner(
            agent=math_agent,
            session_service=self._session_service,
            app_name="a2a_math_agent_app",
        )

    async def execute(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        user_query = context.get_user_input()
        updater = TaskUpdater(event_queue, context.task_id, context.context_id)

        # Create a session for this A2A request
        session_id = str(uuid.uuid4())
        await self._session_service.create_session(
            app_name="a2a_math_agent_app",
            user_id="a2a_user",
            session_id=session_id,
        )

        content = types.Content(
            role="user", parts=[types.Part(text=user_query)]
        )

        print(f"Passing query to ADK Math Agent: '{user_query}'")

        async for event in self._runner.run_async(
            user_id="a2a_user",
            session_id=session_id,
            new_message=content,
        ):
            if event.is_final_response():
                final_text = event.content.parts[0].text
                await updater.add_artifact(
                    [Part(root=TextPart(text=final_text))],
                    name="math_result",
                )
                await updater.complete()
                break

    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise NotImplementedError("Cancellation is not supported.")

# === Server bootstrap ===
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler


if __name__ == "__main__":
    request_handler = DefaultRequestHandler(
        agent_executor=MathAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )
    server_app = A2AStarletteApplication(
        agent_card=math_agent_card,
        http_handler=request_handler,
    )
    print("Starting A2A-enabled Math Agent on http://localhost:10001...")
    uvicorn.run(server_app.build(), host="0.0.0.0", port=10001)