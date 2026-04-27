# File: a2a_handshake/adk_initiator/initiator_agent.py
import httpx
from google.adk.agents import Agent
from a2a.client import A2AClient, A2ACardResolver
from a2a.types import Message, Role, TextPart, Part
import uuid
from a2a.types import SendMessageRequest, MessageSendParams



async def greet_remote_agent(agent_url: str) -> str:
    """Connects to a remote A2A agent, sends a greeting, and returns its response.

    Args:
        agent_url: The URL of the remote A2A agent to greet.
    """
    print(f"Attempting to greet remote agent at {agent_url}...")

    async with httpx.AsyncClient() as httpx_client:
        try:
            # 1. DISCOVER
            print("Step 1: Discovering agent...")
            resolver = A2ACardResolver(httpx_client, agent_url)
            remote_agent_card = await resolver.get_agent_card()
            print(f"--> Discovered agent: '{remote_agent_card.name}'")

            # 2. CONNECT
            print("Step 2: Creating A2A client...")
            a2a_client = A2AClient(httpx_client, agent_card=remote_agent_card)

            # 3. COMMUNICATE
            print("Step 3: Sending message...")
            request_message = Message(
                 message_id=str(uuid.uuid4()),
                 role=Role.user,
                 parts=[Part(root=TextPart(text="Hi from your ADK friend!"))],
            )

            send_request = SendMessageRequest(
                 id=str(uuid.uuid4()),
                  params=MessageSendParams(message=request_message),
                 )
            response = await a2a_client.send_message(send_request)
            task_result = response.root.result

            if (
                task_result
                and task_result.artifacts
                and task_result.artifacts[0].parts
            ):
                final_response = task_result.artifacts[0].parts[0].root.text
                print(f"--> Received response: '{final_response}'")
                return f"Success! The remote agent said: '{final_response}'"

            return "Error: No valid artifact response received."

        except Exception as e:
            print(f"An error occurred: {e}")
            return f"Failed to communicate with agent at {agent_url}."


# Wrap the tool in an Agent so the LLM can call it
initiator_agent = Agent(
    name="Initiator",
    model="gemini-flash-latest",
    instruction="Your job is to greet a remote agent. Use the greet_remote_agent tool.",
    tools=[greet_remote_agent],
)

# ADK runner expects root_agent
root_agent = initiator_agent