from google.adk.agents import LlmAgent
from google.adk.tools import google_search 

from . import prompt 

MODEL = "gemini-2.5-pro" 

market_insight_strategist_agent = LlmAgent(
    name="market_insight_strategist_agent",
    model=MODEL,
    instruction=prompt.MARKET_INSIGHT_STRATEGIST_PROMPT,
    output_key="market_insight_report", 
    tools=[google_search], 
)
