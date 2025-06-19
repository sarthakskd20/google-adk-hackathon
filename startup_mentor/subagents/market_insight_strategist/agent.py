# subagents/market_insight_strategist/agent.py

from google.adk.agents import LlmAgent
from google.adk.tools import google_search # Directly import google_search

from . import prompt # Import prompt.py for the instruction

MODEL = "gemini-2.5-pro-preview-05-06" # Or your chosen model

market_insight_strategist_agent = LlmAgent(
    name="market_insight_strategist_agent",
    model=MODEL,
    instruction=prompt.MARKET_INSIGHT_STRATEGIST_PROMPT,
    output_key="market_insight_report", # This is the output key for this agent
    tools=[google_search], # Directly use google_search here
)