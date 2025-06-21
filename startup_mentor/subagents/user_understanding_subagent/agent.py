from google.adk.tools import FunctionTool
from google.adk.tools.tool_context import ToolContext
from google.adk.agents import LlmAgent
from . import prompt

MODEL = "gemini-2.5-flash"

def validate_response(min_length=3, contains_digits=False):
    def validator(text):
        text = text.strip()
        if len(text) < min_length:
            return False
        if contains_digits and not any(c.isdigit() for c in text):
            return False
        return True
    return validator

# --- Tool Wrapper ---
def create_tool_wrapper(func):
    async def wrapper(tool_context: ToolContext, user_input: str):
        result = func(tool_context, user_input)
        # State is automatically persisted through tool_context.state
        return result
    return wrapper

# --- 1. User Name ---
def collect_user_name(tool_context: ToolContext, user_input: str):
    name = user_input.strip().title()
    if not validate_response(min_length=2)(name):
        return "Could you share what you'd like me to call you? (Even a nickname works!)"
    tool_context.state["user_name"] = name
    return "USER_NAME_COLLECTED"
collect_user_name_tool = FunctionTool(func=collect_user_name)

# --- 2. Age ---
def collect_user_age(tool_context: ToolContext, user_input: str):
    if not validate_response(contains_digits=True)(user_input):
        return "Just so I can give age-appropriate advice, could you share your age range? (e.g., '25-30' or '35')"
    tool_context.state["user_age"] = user_input.strip()
    return "AGE_COLLECTED"
collect_user_age_tool = FunctionTool(func=collect_user_age)

# --- 3. Location ---
def collect_user_location(tool_context: ToolContext, user_input: str):
    if not validate_response(min_length=4)(user_input):
        return "To help with local insights, could you share your nearest city? (e.g., 'Bangalore' or 'Toronto, Canada')"
    tool_context.state["user_location"] = user_input.strip()
    return "LOCATION_COLLECTED"
collect_user_location_tool = FunctionTool(func=collect_user_location)

# --- 4. Background ---
def collect_user_background(tool_context: ToolContext, user_input: str):
    if not validate_response()(user_input):
        return "Tell me about your work/education background in a sentence or two. (e.g., 'I'm a marketing professional with an engineering degree')"
    tool_context.state["user_background"] = user_input.strip()
    return "BACKGROUND_COLLECTED"
collect_user_background_tool = FunctionTool(func=collect_user_background)

# --- 5. Financial Situation ---
def collect_financial_condition(tool_context: ToolContext, user_input: str):
    if not validate_response()(user_input):
        return "To suggest suitable options, could you describe your financial situation? (e.g., 'I can invest $500/month', 'Bootstrapping for now')"
    tool_context.state["user_financial_background"] = user_input.strip()
    return "FINANCIAL_BACKGROUND_COLLECTED"
collect_financial_condition_tool = FunctionTool(func=collect_financial_condition)

# --- 6. Responsibilities ---
def collect_responsibilities(tool_context: ToolContext, user_input: str):
    if not validate_response()(user_input):
        return "What takes up most of your time currently? (Work, family, studies, etc.)"
    tool_context.state["user_responsibilities"] = user_input.strip()
    return "RESPONSIBILITIES_COLLECTED"
collect_responsibilities_tool = FunctionTool(func=collect_responsibilities)

# --- 7. Goals ---
def collect_goals(tool_context: ToolContext, user_input: str):
    if not validate_response()(user_input):
        return "What would make you feel successful in 3-5 years? (Personal or professional)"
    tool_context.state["user_goals"] = user_input.strip()
    return "GOALS_COLLECTED"
collect_goals_tool = FunctionTool(func=collect_goals)

# --- 8. Startup Idea ---
def collect_startup_dream(tool_context: ToolContext, user_input: str):
    if not validate_response()(user_input):
        return "What problem are you excited to solve? (Even vague ideas are welcome!)"
    tool_context.state["user_startup_dream"] = user_input.strip()
    return "STARTUP_DREAM_COLLECTED"
collect_startup_dream_tool = FunctionTool(func=collect_startup_dream)

# --- 9. Time Commitment ---
def collect_available_time(tool_context: ToolContext, user_input: str):
    if not validate_response(contains_digits=True)(user_input):
        return "Roughly how many hours weekly could you dedicate? (e.g., '5-10 hours')"
    tool_context.state["user_available_time"] = user_input.strip()
    return "TIME_AVAILABLE_COLLECTED"
collect_available_time_tool = FunctionTool(func=collect_available_time)

# --- 10. Challenges ---
def collect_challenges(tool_context: ToolContext, user_input: str):
    if not validate_response()(user_input):
        return "What's currently holding you back? (Time, skills, funding, etc.)"
    tool_context.state["user_challenges"] = user_input.strip()
    return "CHALLENGES_COLLECTED"
collect_challenges_tool = FunctionTool(func=collect_challenges)

# --- 11. Mindset ---
def collect_mindset(tool_context: ToolContext, user_input: str):
    if not validate_response()(user_input):
        return "How are you feeling about starting this journey? (Excited, nervous, etc.)"
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
