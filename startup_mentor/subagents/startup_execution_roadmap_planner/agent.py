from google.adk.agents import Agent
from google.adk.tools import google_search 

from . import prompt 

MODEL = "gemini-2.5-pro" 

startup_execution_roadmap_planner_agent = Agent(
    name="startup_execution_roadmap_planner_agent",
    model=MODEL,
    description="This will design a practical roadmap for the user for his startup journey.",
    instruction=prompt.STARTUP_EXECUTION_ROADMAP_PLANNER_PROMPT,
    output_key="startup_roadmap_report", 
    tools=[google_search], 
)
