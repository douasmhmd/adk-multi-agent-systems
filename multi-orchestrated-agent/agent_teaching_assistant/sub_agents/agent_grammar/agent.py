# file: agent_grammar/agent.py
from typing import Optional
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.genai import types

from .prompt import instruction_prompt
from .tools import check_grammar

MODEL = "gemini-2.5-flash"


async def callback_before_agent(
    callback_context: CallbackContext,
) -> Optional[types.Content]:
    """Guardrail: ensure student_profile is loaded before running."""
    if not callback_context.state.get("student_profile"):
        return types.Content(
            role="model",
            parts=[types.Part(text="Error: student_profile not found in state.")],
        )
    return None


agent_grammar = Agent(
    model=MODEL,
    name="agent_grammar",
    description="Checks grammar in student messages.",
    instruction=instruction_prompt,
    tools=[check_grammar],
    output_key="grammar_response",
    before_agent_callback=callback_before_agent,
)