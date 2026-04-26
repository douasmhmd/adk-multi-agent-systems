# file: basic_agent/section2_main_single_agent.py
import asyncio
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService
from google.genai import types

from agent_math.agent import agent_math

load_dotenv()

APP_NAME = "math_app"
USER_ID = "user_1"
SESSION_ID = "session_1"


async def send_query_to_agent(agent, query: str):
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
        artifact_service=InMemoryArtifactService(),
    )

    print(f"User Query: {query}")
    print("-" * 40)

    content = types.Content(role="user", parts=[types.Part(text=query)])
    events = runner.run_async(
        user_id=USER_ID, session_id=SESSION_ID, new_message=content
    )

    async for event in events:
        print(f"Agent: {event.author}")
        is_final_response = event.is_final_response()
        function_calls = event.get_function_calls()
        function_responses = event.get_function_responses()

        if is_final_response:
            final_response = event.content.parts[0].text
            print(f"Final Response: {final_response}")
        elif function_calls:
            for fc in function_calls:
                print(f"Call Function: {fc.name}")
                print(f"Argument: {fc.args}")
        elif function_responses:
            for fr in function_responses:
                print(f"Function Name: {fr.name}")
                print(f"Function Results: {fr.response}")
        print("-" * 40)


if __name__ == "__main__":
    asyncio.run(
        send_query_to_agent(
            agent_math, "First multiply numbers 1 to 3 and then add 4"
        )
    )