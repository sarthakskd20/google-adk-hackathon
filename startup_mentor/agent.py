from typing import AsyncGenerator
from typing_extensions import override
from google.adk.agents import BaseAgent, LlmAgent
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
    instruction = prompt.STARTUP_MENTOR_MAIN_PROMPT,
    description="Provides personalized startup mentorship.",
    tools=[
        AgentTool(agent=legal_foundation_guide_agent),
        AgentTool(agent=market_insight_strategist_agent),
        AgentTool(agent=personalized_financial_architect_agent),
        AgentTool(agent=startup_execution_roadmap_planner_agent),
    ],
)


# ✅ Orchestration Agent
class StartupMentor(BaseAgent):
    name: str = "startup_mentor"
    description: str = "Orchestrates user onboarding and personalized startup mentorship"
    _has_displayed_welcome: bool = False  # Track if welcome message was shown

    @override
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator:
        state = ctx.session.state

        # 🔹 Phase 1: Check if profile is incomplete
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

            # 🔁 Delegate to onboarding agent
            async for event in user_understanding_agent.run_async(ctx):
                yield event

            # 🔒 Recheck after onboarding
            if not is_user_profile_complete(ctx.session.state):
                yield Event(
                    author="agent",
                    content=Content(
                        role="model",
                        parts=[Part(text="📝 I'd love to help you build your startup plan, but I first need to finish understanding you. Let's wrap up the onboarding phase before we move forward!")]
                    )
                )
                return  # ⛔ Exit early — don't proceed

        # ✅ Phase 2: Profile complete, continue with mentorship
        async for event in startup_llm_mentor_agent.run_async(ctx):
            yield event

# Modified coordinator to prevent duplicate flows
class Coordinator(LlmAgent):
    @override
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator:
        # Only let the startup_mentor handle the onboarding flow
        async for event in user_understanding_agent.run_async(ctx):
            yield event

# Create parent agent and assign children via sub_agents
startup_mentor = Coordinator(
    name="startup_mentor",
    model="gemini-2.0-flash",
    description="I coordinate to guide the user with user's profile and user's startup mentor",
    instruction=prompt.STARTUP_MENTOR_MAIN_PROMPT,
    sub_agents=[user_understanding_agent],
    tools=[AgentTool(agent=startup_llm_mentor_agent)],
)

root_agent = startup_mentor
