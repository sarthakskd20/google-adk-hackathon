# subagents/idea_validation_engine/agent.py

from google.adk.agents import LlmAgent
from google.adk.tools import google_search

from . import prompt

MODEL = "gemini-2.5-pro-preview-05-06"  # Or your chosen model

idea_validation_engine_agent = LlmAgent(
    name="idea_validation_engine_agent",
    model=MODEL,
    instruction=prompt.IDEA_VALIDATION_ENGINE_PROMPT,
    output_key="idea_validation_report",
    tools=[google_search],
)