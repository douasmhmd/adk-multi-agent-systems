# File: a2a_math_agent/test_client.py
import asyncio
import uuid
import httpx
from a2a.client import A2AClient, A2ACardResolver
from a2a.types import (
    Message, Role, TextPart, Part,
    SendMessageRequest, MessageSendParams,
)


async def main():
    agent_url = "http://localhost:10001"
    query = "What is 5 times 12?"

    print(f"Sending query to {agent_url}: '{query}'")

    async with httpx.AsyncClient(timeout=60) as httpx_client:
        # Discover
        resolver = A2ACardResolver(httpx_client, agent_url)
        card = await resolver.get_agent_card()
        print(f"Connected to: {card.name}")

        # Send
        client = A2AClient(httpx_client, agent_card=card)
        message = Message(
            message_id=str(uuid.uuid4()),
            role=Role.user,
            parts=[Part(root=TextPart(text=query))],
        )
        request = SendMessageRequest(
            id=str(uuid.uuid4()),
            params=MessageSendParams(message=message),
        )

        response = await client.send_message(request)

        # Check for errors
        if hasattr(response.root, 'error'):
         print(f"\n❌ Server error: {response.root.error}")
         return

        task = response.root.result
        if task and task.artifacts:
            answer = task.artifacts[0].parts[0].root.text
            print(f"\n✅ Math Agent answered:\n{answer}")
        else:
            print("❌ No response received")


if __name__ == "__main__":
    asyncio.run(main())