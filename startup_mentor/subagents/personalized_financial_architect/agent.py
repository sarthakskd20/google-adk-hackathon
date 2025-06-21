from google.adk.agents import Agent
from google.adk.tools import google_search

from . import prompt 

MODEL = "gemini-2.5-pro" 

personalized_financial_architect_agent = Agent(
    name="personalized_financial_architect_agent",
    model=MODEL,
    description="This is your personal financial architect which will plan a financial plan for the user properly",
    instruction=prompt.PERSONALIZED_FINANCIAL_ARCHITECT_PROMPT,
    output_key="personalized_financial_plan", 
    tools=[google_search]
)
