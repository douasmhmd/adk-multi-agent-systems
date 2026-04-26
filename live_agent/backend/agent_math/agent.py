# file: agent_math/agent.py
from google.adk.agents import Agent
from google.genai import types

from .tools import add, subtract, multiply, divide
from .prompt import instruction_prompt
from .context import context
from .examples import examples

MODEL = "gemini-2.5-flash"


def create_math_agent(model=MODEL):
    context["examples"] = examples

    math_agent = Agent(
        model=model,
        name="agent_math",
        description="A friendly math tutor for kids.",
        instruction=instruction_prompt,
        tools=[add, subtract, multiply, divide],
        generate_content_config=types.GenerateContentConfig(temperature=0.2),
    )

    return math_agent, context