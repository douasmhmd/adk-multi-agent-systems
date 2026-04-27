# File: specialist_agents/researcher/server.py
import uuid
from dotenv import load_dotenv

from a2a.types import (
    AgentCard, AgentSkill, AgentCapabilities, Part, TextPart,
)
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.tasks import TaskUpdater, InMemoryTaskStore
from a2a.server.events import EventQueue
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import uvicorn

from agent_logic import root_agent

load_dotenv()


agent_card = AgentCard(
    name="ADK Researcher",
    description="Researches topics by searching the web.",
    url="http://localhost:10003/",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=True),
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
    skills=[
        AgentSkill(
            id="research",
            name="Research a Topic",
            description="Searches the web and summarizes findings.",
            tags=["research", "search"],
            examples=["AI healthcare trends", "climate solutions"],
        )
    ],
)


class ResearcherExecutor(AgentExecutor):
    def __init__(self):
        self._session_service = InMemorySessionService()
        self._runner = Runner(
            agent=root_agent,
            session_service=self._session_service,
            app_name="researcher_app",
        )

    async def execute(self, context: RequestContext, event_queue: EventQueue):
        query = context.get_user_input()
        updater = TaskUpdater(event_queue, context.task_id, context.context_id)

        session_id = str(uuid.uuid4())
        await self._session_service.create_session(
            app_name="researcher_app",
            user_id="a2a_user",
            session_id=session_id,
        )

        content = types.Content(
            role="user", parts=[types.Part(text=query)]
        )

        print(f"Researcher received query: '{query}'")

        async for event in self._runner.run_async(
            user_id="a2a_user",
            session_id=session_id,
            new_message=content,
        ):
            if event.is_final_response():
                final_text = event.content.parts[0].text
                await updater.add_artifact(
                    [Part(root=TextPart(text=final_text))],
                    name="research_result",
                )
                await updater.complete()
                break

    async def cancel(self, context, event_queue):
        raise NotImplementedError()


if __name__ == "__main__":
    handler = DefaultRequestHandler(
        agent_executor=ResearcherExecutor(),
        task_store=InMemoryTaskStore(),
    )
    app = A2AStarletteApplication(agent_card=agent_card, http_handler=handler)
    print("Starting ADK Researcher Agent on http://localhost:10003...")
    uvicorn.run(app.build(), host="0.0.0.0", port=10003)