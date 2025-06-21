# subagents/startup_execution_roadmap_planner/agent.py

from google.adk.agents import LlmAgent
from google.adk.tools import google_search # Keep Google Search as a potential fallback tool if needed

from . import prompt # Import prompt.py for the instruction

MODEL = "gemini-2.5-pro-preview-05-06" # Or your chosen model

startup_execution_roadmap_planner_agent = LlmAgent(
    name="startup_execution_roadmap_planner_agent",
    model=MODEL,
    instruction=prompt.STARTUP_EXECUTION_ROADMAP_PLANNER_PROMPT,
    output_key="startup_roadmap_report", # This is the output key for this agent
    tools=[google_search], # Google Search available for edge cases or clarifications during synthesis
)