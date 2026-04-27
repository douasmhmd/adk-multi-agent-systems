# File: research_coordinator/agent.py
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from a2a_tools import delegate_research

coordinator_agent = Agent(
    name="ResearchCoordinator",
    model=LiteLlm(model="openai/gpt-4o-mini"),
    description="Coordinates research by delegating to specialist agents via A2A.",
    instruction="""
    You are a research coordinator. When the user gives you a topic to research,
    use the delegate_research tool which will:
    1. Generate search queries from the topic
    2. Research each query
    3. Return synthesized findings
    Then present the results to the user clearly.
    """,
    tools=[delegate_research],
)

root_agent = coordinator_agent