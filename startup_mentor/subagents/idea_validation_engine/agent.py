from google.adk.agents import Agent
from google.adk.tools import google_search

from . import prompt

MODEL = "gemini-2.5-pro" 

idea_validation_engine_agent = Agent(
    name="idea_validation_engine_agent",
    model=MODEL,
    description="analyzes the startup_idea of the user, analyzes it, and guides the user for the improvements and judges it whether it is a good idea or not",
    instruction=prompt.IDEA_VALIDATION_ENGINE_PROMPT,
    output_key="idea_validation_report",
    tools=[google_search],
)
