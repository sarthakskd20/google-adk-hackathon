from google.adk.agents import Agent
from google.adk.tools import google_search

from . import prompt

MODEL = "gemini-2.5-pro"  

current_opportunity_finder_agent = Agent(
    name="current_opportunity_finder_agent",
    model=MODEL,
    description="It searches the with the help of google search and finds the current available opportunities for their startup journey and guides the user.",
    instruction=prompt.CURRENT_OPPORTUNITY_FINDING_PROMPT,
    output_key="current_opportunities_finder-output",
    tools=[google_search],
)
