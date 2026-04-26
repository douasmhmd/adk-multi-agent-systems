# file: agent_teaching_assistant/agent.py
from typing import Optional
from google.adk.agents import SequentialAgent
from google.adk.agents.callback_context import CallbackContext
from google.genai import types

from .context import context
from .sub_agents.agent_grammar.agent import agent_grammar
from .sub_agents.agent_math.agent import agent_math
from .sub_agents.agent_summary.agent import agent_summary


async def callback_before_agent(
    callback_context: CallbackContext,
) -> Optional[types.Content]:
    """Inject the student profile into session state on first run."""
    if not callback_context.state.get("student_profile"):
        try:
            callback_context.state["student_profile"] = context["student_profile"]
        except Exception as e:
            print(f"Error loading student profile: {e}")
            return types.Content(
                role="model",
                parts=[types.Part(text="Error: Cannot find student profile.")],
            )
    return None


async def callback_after_agent(
    callback_context: CallbackContext,
) -> Optional[types.Content]:
    """Optional: log when pipeline completes."""
    print("Pipeline completed successfully.")
    return None


root_agent = SequentialAgent(
    name="agent_teaching_assistant",
    description="A teaching assistant that checks grammar, solves math, and summarizes for kids.",
    sub_agents=[agent_grammar, agent_math, agent_summary],
    before_agent_callback=callback_before_agent,
    after_agent_callback=callback_after_agent,
)