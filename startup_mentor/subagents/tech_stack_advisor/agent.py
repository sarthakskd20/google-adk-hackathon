# subagents/tech_stack_advisor/agent.py
from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from . import prompt

MODEL = "gemini-2.5-pro-preview-05-06"

tech_stack_advisor_agent = LlmAgent(
    name="tech_stack_advisor_agent",
    model=MODEL,
    instruction=prompt.TECH_STACK_ADVISOR_PROMPT,
    output_key="tech_stack_report",
    tools=[google_search],
)