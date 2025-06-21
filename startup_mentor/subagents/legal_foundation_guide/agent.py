# subagents/legal_foundation_guide/agent.py

from google.adk.agents import LlmAgent
from google.adk.tools import google_search
# No AgentTool import needed here as this agent does not call other sub-agents or tools.

from . import prompt # Import prompt.py for the instruction
# from . import tools # Not directly used for agent definition, as no tools are used.

MODEL = "gemini-2.5-pro-preview-05-06" # Or your chosen model

legal_foundation_guide_agent = LlmAgent(
    name="legal_foundation_guide_agent",
    model=MODEL,
    instruction=prompt.LEGAL_FOUNDATION_GUIDE_PROMPT,
    output_key="legal_foundation_report", # This is the output key for this agent
    tools=[google_search], # This agent does NOT use any external tools or FunctionTools.
)