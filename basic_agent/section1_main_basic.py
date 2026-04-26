# file: basic_agent/section1_main_basic.py
import asyncio
import time
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

load_dotenv()

basic_agent = Agent(
    name="basic_agent",
    model="gemini-2.5-flash",
    description="A simple conversational agent.",
    instruction="You are a friendly and helpful assistant."
)

APP_NAME = "basic_app"
USER_ID = "user_1"
SESSION_ID = "session_1"


async def main():
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    ) # the Runner is the engine that executes it. It orchestrates the entire interaction:
    runner = Runner(
        agent=basic_agent, app_name=APP_NAME, session_service=session_service
    ) #  the Runner doesn’t return a single answer, but rather a stream of events.

    query = "Hi, how are you?"
    print(f"User Query: {query}")
    print("- " * 15)

    content = types.Content(role="user", parts=[types.Part(text=query)])
    start = time.time()

    async for event in runner.run_async(
        user_id=USER_ID, session_id=SESSION_ID, new_message=content
    ):
        if event.is_final_response():
            elapsed = (time.time() - start) * 1000
            print(">>> Inside final response <<<")
            print("- " * 15)
            print(f"Agent: {event.author}")
            print(f"Response time: {elapsed:.3f} ms")
            print(f"Final Response:\n{event.content.parts[0].text}")


if __name__ == "__main__":
    asyncio.run(main())