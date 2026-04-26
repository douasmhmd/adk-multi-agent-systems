# file: agent_math/agent.py
from typing import Optional
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.genai import types

from .prompt import instruction_prompt
from .tools import add, subtract, multiply, divide
from .examples import examples

MODEL = "gemini-2.5-flash"


async def callback_before_agent(
    callback_context: CallbackContext,
) -> Optional[types.Content]:
    """Guardrails: ensure student profile and grammar response exist."""
    if not callback_context.state.get("student_profile"):
        return types.Content(
            role="model",
            parts=[types.Part(text="Error: student_profile not found.")],
        )

    if not callback_context.state.get("grammar_response"):
        return types.Content(
            role="model",
            parts=[types.Part(text="Error: Grammar agent hasn't run yet.")],
        )

    if not callback_context.state.get("math_examples"):
        callback_context.state["math_examples"] = examples

    return None


agent_math = Agent(
    model=MODEL,
    name="agent_math",
    description="Solves math problems for kids.",
    instruction=instruction_prompt,
    tools=[add, subtract, multiply, divide],
    output_key="math_response",
    before_agent_callback=callback_before_agent,
)