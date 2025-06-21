from google.adk.agents import Agent
from google.adk.tools import google_search 


from . import prompt 

MODEL = "gemini-2.5-pro" 

market_insight_strategist_agent = Agent(
    name="market_insight_strategist_agent",
    model=MODEL,
    description="analyzes the market insight and strategises things and helps user for their startup by the recommending the additions and improvements with the current market states.",
    instruction=prompt.MARKET_INSIGHT_STRATEGIST_PROMPT,
    output_key="market_insight_report", 
    tools=[google_search], 
)
