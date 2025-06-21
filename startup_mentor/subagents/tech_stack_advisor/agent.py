
from google.adk.agents import Agent

from google.adk.tools import google_search
from . import prompt

MODEL = "gemini-2.5-pro"


tech_stack_advisor_agent = Agent(
    name="tech_stack_advisor_agent",
    model=MODEL,
    description="It will provide the user personalized, actionable technology recommendations.",
    instruction=prompt.TECH_STACK_ADVISOR_PROMPT,
    output_key="tech_stack_report",
    tools=[google_search],
)
