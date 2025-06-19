# subagents/personalized_financial_architect/agent.py

from google.adk.agents import LlmAgent

from . import prompt # Import prompt.py for the instruction

MODEL = "gemini-2.5-pro-preview-05-06" # Or your chosen model

personalized_financial_architect_agent = LlmAgent(
    name="personalized_financial_architect_agent",
    model=MODEL,
    instruction=prompt.PERSONALIZED_FINANCIAL_ARCHITECT_PROMPT,
    output_key="personalized_financial_plan", # This is the output key for this agent
)