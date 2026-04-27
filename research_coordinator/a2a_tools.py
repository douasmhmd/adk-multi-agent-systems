# File: research_coordinator/a2a_tools.py
import uuid
import httpx
from a2a.client import A2AClient, A2ACardResolver
from a2a.types import (
    Message, Role, TextPart, Part,
    SendMessageRequest, MessageSendParams,
)


QUERY_GENERATOR_URL = "http://localhost:10002"
RESEARCHER_URL = "http://localhost:10003"


async def call_remote_agent(httpx_client, agent_url: str, query: str) -> str:
    """Helper: call a remote A2A agent and return the artifact text."""
    resolver = A2ACardResolver(httpx_client, agent_url)
    card = await resolver.get_agent_card()
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

    if hasattr(response.root, "error"):
        return f"Error from {card.name}: {response.root.error}"

    task = response.root.result
    if task and task.artifacts:
        return task.artifacts[0].parts[0].root.text
    return "No response received."


async def delegate_research(research_topic: str) -> str:
    """Orchestrates a team of A2A agents to research a topic and return a summary.

    Args:
        research_topic: The high-level topic to be researched.

    Returns:
        A consolidated string with search queries and their research findings.
    """
    print(f"--- Starting research for: '{research_topic}' ---")
    all_search_results = ""

    async with httpx.AsyncClient(timeout=120) as httpx_client:
        try:
            # Step 1: Get queries from QueryGenerator (LangGraph)
            print("\nStep 1: Delegating to QueryGeneratorAgent (LangGraph)...")
            queries_text = await call_remote_agent(
                httpx_client,
                QUERY_GENERATOR_URL,
                research_topic,
            )
            print(f"--> Received queries:\n{queries_text}")

            # Parse query lines (format: "- query text")
            search_queries = [
                line.lstrip("- ").strip()
                for line in queries_text.split("\n")
                if line.strip()
            ]

            # Step 2: Research each query via Researcher (ADK)
            print("\nStep 2: Delegating to ResearcherAgent (ADK)...")
            for query in search_queries:
                print(f"  - Executing query: '{query}'")
                result = await call_remote_agent(
                    httpx_client,
                    RESEARCHER_URL,
                    query,
                )
                all_search_results += f"### {query}\n{result}\n\n"

            # Step 3: Return raw results - the coordinator's LLM will synthesize
            return (
                f"Research data collected for topic '{research_topic}':\n\n"
                f"{all_search_results}\n\n"
                f"Please synthesize this data into a 3-paragraph summary."
            )

        except Exception as e:
            return f"An error occurred during research: {e}"