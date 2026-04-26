# file: agent_summary/agent.py
from typing import Optional
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.genai import types

from .prompt import instruction_prompt

MODEL = "gemini-2.5-flash"


async def callback_before_agent(
    callback_context: CallbackContext,
) -> Optional[types.Content]:
    """Guardrails: ensure both previous agents have run."""
    if not callback_context.state.get("grammar_response"):
        return types.Content(
            role="model",
            parts=[types.Part(text="Error: Grammar response missing.")],
        )

    if not callback_context.state.get("math_response"):
        return types.Content(
            role="model",
            parts=[types.Part(text="Error: Math response missing.")],
        )

    return None


agent_summary = Agent(
    model=MODEL,
    name="agent_summary",
    description="Combines responses from grammar and math agents.",
    instruction=instruction_prompt,
    output_key="summary_response",
    before_agent_callback=callback_before_agent,
)