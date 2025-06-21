from google.adk.agents import Agent
from google.adk.tools import google_search

from . import prompt 
MODEL = "gemini-2.5-pro" 

legal_foundation_guide_agent = Agent(
    name="legal_foundation_guide_agent",
    model=MODEL,
    description="It guides the user with the legal documents and awares user with the legal guidance required for their startup.",
    instruction=prompt.LEGAL_FOUNDATION_GUIDE_PROMPT,
    output_key="legal_foundation_report", 
    tools=[google_search], 
    )
