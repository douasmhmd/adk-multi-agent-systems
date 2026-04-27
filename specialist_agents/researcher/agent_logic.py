# File: specialist_agents/researcher/agent_logic.py
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm


def search_web(query: str) -> dict:
    """Searches the web for information about a query.

    Args:
        query: The search query string.

    Returns:
        A dictionary with the search results.
    """
    return {
        "query": query,
        "results": [
            f"Result 1 for '{query}': This is a relevant article snippet.",
            f"Result 2 for '{query}': Another useful piece of information.",
            f"Result 3 for '{query}': A third source confirming the topic.",
        ],
    }


root_agent = Agent(
    model=LiteLlm(model="openai/gpt-4o-mini"),
    name="researcher",
    description="Researches topics by searching the web.",
    instruction="""
    You are a research assistant. When given a search query, use the search_web
    tool to find information, then summarize the key findings in 2-3 sentences.
    """,
    tools=[search_web],
)