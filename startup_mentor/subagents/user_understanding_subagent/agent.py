from google.adk.tools import FunctionTool
from google.adk.tools.tool_context import ToolContext
from google.adk.agents import LlmAgent
from . import prompt

MODEL = "gemini-2.5-flash"

# --- 1. User Name ---
def collect_user_name(tool_context: ToolContext, user_input: str):
    name = user_input.strip().title()
    if len(name) < 2:
        return "Just checking, could you share your name again? 😊"
    tool_context.state["user_name"] = user_input
    return "USER_NAME_COLLECTED"
collect_user_name_tool = FunctionTool(func=collect_user_name)

# --- 2. Age (as string) ---
def collect_user_age(tool_context: ToolContext, user_input: str):
    if not any(char.isdigit() for char in user_input):
        return "Could you please share your age in years?"
    tool_context.state["user_age"] = user_input.strip()
    return "AGE_COLLECTED"
collect_user_age_tool = FunctionTool(func=collect_user_age)

# --- 3. Location ---
def collect_user_location(tool_context: ToolContext, user_input: str):
    location = user_input.strip()
    if len(location.split()) < 2:
        return "Could you tell me your city and state/country together? (e.g., 'Indore Madhya Pradesh')"
    tool_context.state["user_location"] = location
    return "LOCATION_COLLECTED"
collect_user_location_tool = FunctionTool(func=collect_user_location)

# --- 4. Background (Education + Profession) ---
def collect_user_background(tool_context: ToolContext, user_input: str):
    if len(user_input.strip()) < 5:
        return "Tell me a bit more about your education or job background."
    tool_context.state["user_background"] = user_input.strip()
    return "BACKGROUND_COLLECTED"
collect_user_background_tool = FunctionTool(func=collect_user_background)

# --- 5. Financial Background ---
def collect_financial_condition(tool_context: ToolContext, user_input: str):
    tool_context.state["user_financial_background"] = user_input.strip()
    return "FINANCIAL_BACKGROUND_COLLECTED"
collect_financial_condition_tool = FunctionTool(func=collect_financial_condition)

# --- 6. Primary Responsibility ---
def collect_responsibilities(tool_context: ToolContext, user_input: str):
    if len(user_input.strip()) < 5:
        return "Would you like to share your biggest responsibility in life currently?"
    tool_context.state["user_primary_responsibility"] = user_input.strip()
    return "RESPONSIBILITY_COLLECTED"
collect_responsibilities_tool = FunctionTool(func=collect_responsibilities)

# --- 7. Goals ---
def collect_goals(tool_context: ToolContext, user_input: str):
    if len(user_input.strip()) < 5:
        return "Feel free to describe your main goal or dream in life!"
    tool_context.state["user_goal"] = user_input.strip()
    return "GOAL_COLLECTED"
collect_goals_tool = FunctionTool(func=collect_goals)

# --- 8. Startup Dream ---
def collect_startup_dream(tool_context: ToolContext, user_input: str):
    if len(user_input.strip()) < 5:
        return "What's something you'd love to build or solve with your startup?"
    tool_context.state["user_startup_dream"] = user_input.strip()
    return "STARTUP_DREAM_COLLECTED"
collect_startup_dream_tool = FunctionTool(func=collect_startup_dream)

# --- 9. Time Available ---
def collect_available_time(tool_context: ToolContext, user_input: str):
    if not any(char.isdigit() for char in user_input):
        return "How much time (hours/week) could you devote to your startup journey?"
    tool_context.state["user_available_time"] = user_input.strip()
    return "TIME_AVAILABLE_COLLECTED"
collect_available_time_tool = FunctionTool(func=collect_available_time)

# --- 10. Challenges ---
def collect_challenges(tool_context: ToolContext, user_input: str):
    if len(user_input.strip()) < 5:
        return "Are there any current challenges or personal struggles you'd like to share?"
    tool_context.state["user_challenges"] = user_input.strip()
    return "CHALLENGES_COLLECTED"
collect_challenges_tool = FunctionTool(func=collect_challenges)

# --- 11. Mental Readiness ---
def collect_mindset(tool_context: ToolContext, user_input: str):
    if len(user_input.strip()) < 5:
        return "How are you feeling mentally or emotionally about starting something on your own?"
    tool_context.state["user_mindset"] = user_input.strip()
    return "MINDSET_COLLECTED"
collect_mindset_tool = FunctionTool(func=collect_mindset)

# --- Assembling the Agent ---
user_understanding_agent = LlmAgent(
    name="user_understanding_agent",
    model=MODEL,
    instruction=prompt.USER_UNDERSTANDING_PROMPT,
    tools=[
        collect_user_name_tool,
        collect_user_age_tool,
        collect_user_location_tool,
        collect_user_background_tool,
        collect_financial_condition_tool,
        collect_responsibilities_tool,
        collect_goals_tool,
        collect_startup_dream_tool,
        collect_available_time_tool,
        collect_challenges_tool,
        collect_mindset_tool,
    ],
    output_key="user_understanding"
)
