from google.adk.agents import LlmAgent
from google.adk.tools import google_search

from . import prompt

MODEL = "gemini-2.5-pro-preview-05-06"  

current_opportunity_finder_agent = LlmAgent(
    name="idea_validation_engine_agent",
    model=MODEL,
    instruction=prompt.CURRENT_OPPORTUNITY_FINDING_PROMPT,
    output_key="current_opportunities_finder-output",
    tools=[google_search],
)
