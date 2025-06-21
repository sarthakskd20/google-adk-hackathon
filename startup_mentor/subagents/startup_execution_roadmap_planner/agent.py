from google.adk.agents import LlmAgent
from google.adk.tools import google_search 
from . import prompt 

MODEL = "gemini-2.5-pro" 

startup_execution_roadmap_planner_agent = LlmAgent(
    name="startup_execution_roadmap_planner_agent",
    model=MODEL,
    instruction=prompt.STARTUP_EXECUTION_ROADMAP_PLANNER_PROMPT,
    output_key="startup_roadmap_report", 
    tools=[google_search], 
)
