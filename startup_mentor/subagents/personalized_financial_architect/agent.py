from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from . import prompt 

MODEL = "gemini-2.5-pro-preview-05-06" 

personalized_financial_architect_agent = LlmAgent(
    name="personalized_financial_architect_agent",
    model=MODEL,
    instruction=prompt.PERSONALIZED_FINANCIAL_ARCHITECT_PROMPT,
    output_key="personalized_financial_plan", 
    tools=[google_search]
)
