from google.adk.agents import LlmAgent
from google.adk.tools import google_search

from . import prompt 
MODEL = "gemini-2.5-pro-preview-05-06" 

legal_foundation_guide_agent = LlmAgent(
    name="legal_foundation_guide_agent",
    model=MODEL,
    instruction=prompt.LEGAL_FOUNDATION_GUIDE_PROMPT,
    output_key="legal_foundation_report", 
    tools=[google_search], 
    )
