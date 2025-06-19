# main.py

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
# Import the new sub-agents.
# Ensure these files exist in your 'subagents' directory and export their respective Agent instances.
from .subagents.legal_foundation_guide import legal_foundation_guide_agent
from .subagents.market_insight_strategist import market_insight_strategist_agent
from .subagents.startup_execution_roadmap_planner import startup_execution_roadmap_planner_agent
from .subagents.personalized_financial_architect import personalized_financial_architect_agent

MODEL = "gemini-2.5-pro-preview-05-06"

# --- Main Startup Mentor Agent (Orchestration Pipeline) ---

# This is your new primary agent that orchestrates the entire mentorship journey
# by calling the composite agents in a predefined sequence.
startup_mentor = LlmAgent(
    name="startup_mentor", # Renamed to better reflect its role as an orchestrator
    model=MODEL,
    description=(
        "Acts as a supportive and knowledgeable mentor for beginner entrepreneurs. "
        "It guides users step-by-step through startup ideation, validation, planning, "
        "execution, and financial strategy by orchestrating specialized sub-agents "
    ),
    # The order here defines the workflow: first initial analysis, then planning.
    tools=[
        AgentTool(agent=startup_execution_roadmap_planner_agent),
        AgentTool(agent=legal_foundation_guide_agent),
        AgentTool(agent=market_insight_strategist_agent),
        AgentTool(agent=personalized_financial_architect_agent),
    ],
    # No direct instruction needed here if its role is purely orchestration.
    # The instructions are handled by the sub-agents and their respective prompts.
)

# The root_agent for ADK web or direct execution will be this main orchestrator.
root_agent = startup_mentor