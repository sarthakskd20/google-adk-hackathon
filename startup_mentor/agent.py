from typing import AsyncGenerator
from typing_extensions import override
from google.adk.agents import BaseAgent, LlmAgent, SequentialAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.tools.agent_tool import AgentTool
from google.adk.events import Event
from google.genai.types import Content, Part

from . import prompt
from .subagents.user_understanding_subagent import user_understanding_agent
from .subagents.legal_foundation_guide import legal_foundation_guide_agent
from .subagents.market_insight_strategist import market_insight_strategist_agent
from .subagents.personalized_financial_architect import personalized_financial_architect_agent
from .subagents.startup_execution_roadmap_planner import startup_execution_roadmap_planner_agent
from .subagents.idea_validation_engine import idea_validation_engine_agent
from .subagents.tech_stack_advisor import tech_stack_advisor_agent

# ✅ Helper to check onboarding state completeness
def is_user_profile_complete(state: dict) -> bool:
    required_fields = [
        "user_name",
        "user_age",
        "user_location",
        "user_background",
        "user_financial_background",
        "user_responsibilities",
        "user_goals",
        "user_startup_dream",
        "user_available_time",
        "user_challenges",
        "user_mindset",
    ]
    return all(state.get(field) for field in required_fields)

# ✅ Startup mentorship LLM agent
startup_llm_mentor_agent = LlmAgent(
    name="startup_llm_mentor",
    model="gemini-2.0-flash",
    instruction=prompt.STARTUP_MENTOR_MAIN_PROMPT,
    description="Provides personalized startup mentorship.",
    tools=[
        AgentTool(agent=startup_execution_roadmap_planner_agent),
        AgentTool(agent=market_insight_strategist_agent),
        AgentTool(agent=legal_foundation_guide_agent),
        AgentTool(agent=personalized_financial_architect_agent),
        AgentTool(agent=idea_validation_engine_agent),
        AgentTool(agent=tech_stack_advisor_agent),
    ],
)

# ✅ Custom Orchestrator Agent
class StartupMentorOrchestrator(BaseAgent):
    """
    Custom agent for startup mentorship workflow.
    
    This agent orchestrates the user onboarding and startup mentorship process,
    ensuring proper coordination between the user understanding agent and the
    startup mentor agent.
    """
    
    # Field declarations
    user_understanding_agent: BaseAgent
    startup_mentor_agent: LlmAgent
    
    def __init__(
        self,
        name: str,
        user_understanding_agent: BaseAgent,
        startup_mentor_agent: LlmAgent,
    ):
        """
        Initializes the StartupMentorOrchestrator.
        
        Args:
            name: The name of the agent.
            user_understanding_agent: The agent for user onboarding.
            startup_mentor_agent: The agent for startup mentorship.
        """
        # Define the sub_agents list for the framework
        sub_agents_list = [
            user_understanding_agent,
            startup_mentor_agent,
        ]
        
        super().__init__(
            name=name,
            user_understanding_agent=user_understanding_agent,
            startup_mentor_agent=startup_mentor_agent,
            sub_agents=sub_agents_list,
        )
        self._has_displayed_welcome = False  # Track if welcome message was shown

    @override
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator:
        state = ctx.session.state

        # Phase 1: Check if profile is incomplete
        if not is_user_profile_complete(state):
            # Only show welcome message if it hasn't been shown yet
            if not self._has_displayed_welcome:
                yield Event(
                    author="agent",
                    content=Content(
                        role="model",
                        parts=[Part(text="👋 Hi there! I'm excited to guide you. Let's begin by understanding you a little better.")]
                    )
                )
                self._has_displayed_welcome = True

            # Delegate COMPLETELY to onboarding agent
            async for event in self.user_understanding_agent.run_async(ctx):
                yield event
                # Update state after each event
                state = ctx.session.state

            # After onboarding completes, check if we can proceed
            if is_user_profile_complete(state):
                yield Event(
                    author="agent",
                    content=Content(
                        role="model",
                        parts=[Part(text="✅ Great! Now that I understand you better, let's work on your startup plan!")]
                    )
                )
            else:
                # If still incomplete, let the user continue the conversation
                return

        # Phase 2: Profile complete, continue with mentorship
        if is_user_profile_complete(state):
            async for event in self.startup_mentor_agent.run_async(ctx):
                yield event

# Create the custom orchestrator agent instance
startup_mentor_orchestrator = StartupMentorOrchestrator(
    name="startup_mentor_orchestrator",
    user_understanding_agent=user_understanding_agent,
    startup_mentor_agent=startup_llm_mentor_agent,
)

root_agent = startup_mentor_orchestrator
