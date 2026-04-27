# File: a2a_handshake/adk_initiator/main.py
import asyncio
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from initiator_agent import root_agent

load_dotenv()

APP_NAME = "initiator_app"
USER_ID = "test_user"
SESSION_ID = "session_1"


async def main():
    """Runs the Initiator agent to greet the remote Greeter agent."""
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    query = "Please greet the agent at http://localhost:10000"
    content = types.Content(role="user", parts=[types.Part(text=query)])

    print(f"--- Running ADK Initiator with query: '{query}' ---")

    async for event in runner.run_async(
        user_id=USER_ID, session_id=SESSION_ID, new_message=content
    ):
        if event.is_final_response():
            print("\n--- Final Response from Initiator ---")
            print(event.content.parts[0].text)


if __name__ == "__main__":
    asyncio.run(main())