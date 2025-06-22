from google.adk.tools import FunctionTool
from google.adk.tools.tool_context import ToolContext
from google.adk.sessions import InMemorySessionService, Session
from google.adk.agents import LlmAgent
from . import prompt

MODEL = "gemini-2.0-pro"

# --- 1. User Name ---
def collect_user_name(user_input: str, tool_context: ToolContext) -> dict:
    """Collect and validate the user's name.
    
    Args:
        user_input: The name provided by the user
        tool_context: Context for accessing and updating session state
        
    Returns:
        A response dictionary with status and message
    """
    name = user_input.strip().title()
    tool_context.state["user_name"] = name
    user_name = tool_context.state["user_name"]
    return {
        "status": "success",
        "action": "collect_user_name",
        "collected_value": user_name,
        "message": "USER_NAME_COLLECTED"
    }

# --- 2. Age ---
def collect_user_age(user_input: str, tool_context: ToolContext) -> dict:
    """Collect and validate the user's age.
    
    Args:
        user_input: The age provided by the user
        tool_context: Context for accessing and updating session state
        
    Returns:
        A response dictionary with status and message
    """
    tool_context.state["user_age"] = user_input
    user_age = tool_context.state["user_age"]
    return {
        "status": "success",
        "action": "collect_user_age",
        "collected_value": user_age,
        "message": "AGE_COLLECTED"
    }

# --- 3. Location ---
def collect_user_location(user_input: str, tool_context: ToolContext) -> dict:
    """Collect and validate the user's location.
    
    Args:
        user_input: The location provided by the user
        tool_context: Context for accessing and updating session state
        
    Returns:
        A response dictionary with status and message
    """
    
    tool_context.state["user_location"] = user_input
    user_location = tool_context.state["user_location"]
    return {
        "status": "success",
        "action": "collect_user_location",
        "collected_value": user_location,
        "message": "LOCATION_COLLECTED"
    }

# --- 4. Background ---
def collect_user_background(user_input: str, tool_context: ToolContext) -> dict:
    """Collect and validate the user's background information.
    
    Args:
        user_input: The background information provided by the user
        tool_context: Context for accessing and updating session state
        
    Returns:
        A response dictionary with status and message
    """
    
    tool_context.state["user_background"] = user_input
    user_background = tool_context.state["user_background"]
    return {
        "status": "success",
        "action": "collect_user_background",
        "collected_value": user_background,
        "message": "BACKGROUND_COLLECTED"
    }

# --- 5. Financial Situation ---
def collect_financial_condition(user_input: str, tool_context: ToolContext) -> dict:
    """Collect and validate the user's financial situation.
    
    Args:
        user_input: The financial information provided by the user
        tool_context: Context for accessing and updating session state
        
    Returns:
        A response dictionary with status and message
    """
    tool_context.state["user_financial_background"] = user_input
    user_financial_background = tool_context.state["user_financial_background"]
    return {
        "status": "success",
        "action": "collect_financial_condition",
        "collected_value": user_financial_background,
        "message": "FINANCIAL_BACKGROUND_COLLECTED"
    }

# --- 6. Responsibilities ---
def collect_responsibilities(user_input: str, tool_context: ToolContext) -> dict:
    """Collect and validate the user's responsibilities.
    
    Args:
        user_input: The responsibilities information provided by the user
        tool_context: Context for accessing and updating session state
        
    Returns:
        A response dictionary with status and message
    """
    
    tool_context.state["user_responsibilities"] = user_input
    user_responsibilities = tool_context.state["user_responsibilities"]
    return {
        "status": "success",
        "action": "collect_responsibilities",
        "collected_value": user_responsibilities,
        "message": "RESPONSIBILITIES_COLLECTED"
    }



# --- 8. Startup Idea ---
def collect_startup_dream(user_input: str, tool_context: ToolContext) -> dict:
    """Collect and validate the user's startup idea.
    
    Args:
        user_input: The startup idea provided by the user
        tool_context: Context for accessing and updating session state
        
    Returns:
        A response dictionary with status and message
    """
    
    tool_context.state["user_startup_dream"] = user_input
    user_startup_dream = tool_context.state["user_startup_dream"]
    return {
        "status": "success",
        "action": "collect_startup_dream",
        "collected_value": user_startup_dream,
        "message": "STARTUP_DREAM_COLLECTED"
    }

# --- 9. Time Commitment ---
def collect_available_time(user_input: str, tool_context: ToolContext) -> dict:
    """Collect and validate the user's available time commitment.
    
    Args:
        user_input: The time commitment information provided by the user
        tool_context: Context for accessing and updating session state
        
    Returns:
        A response dictionary with status and message
    """
    
    tool_context.state["user_available_time"] = user_input
    user_available_time = tool_context.state["user_available_time"]
    return {
        "status": "success",
        "action": "collect_available_time",
        "collected_value": user_available_time,
        "message": "TIME_AVAILABLE_COLLECTED"
    }

# --- 10. Challenges ---
def collect_challenges(user_input: str, tool_context: ToolContext) -> dict:
    """Collect and validate the user's challenges.
    
    Args:
        user_input: The challenges information provided by the user
        tool_context: Context for accessing and updating session state
        
    Returns:
        A response dictionary with status and message
    """
    
    tool_context.state["user_challenges"] = user_input
    user_challenges = tool_context.state["user_challenges"]
    return {
        "status": "success",
        "action": "collect_challenges",
        "collected_value": user_challenges,
        "message": "CHALLENGES_COLLECTED"
    }


# --- Create Tool Instances ---
collect_user_name_tool = FunctionTool(func=collect_user_name)
collect_user_age_tool = FunctionTool(func=collect_user_age)
collect_user_location_tool = FunctionTool(func=collect_user_location)
collect_user_background_tool = FunctionTool(func=collect_user_background)
collect_financial_condition_tool = FunctionTool(func=collect_financial_condition)
collect_responsibilities_tool = FunctionTool(func=collect_responsibilities)
collect_startup_dream_tool = FunctionTool(func=collect_startup_dream)
collect_available_time_tool = FunctionToolfunc=(collect_available_time)
collect_challenges_tool = FunctionTool(func=collect_challenges)

# --- Assembling the Agent ---
user_understanding_agent = LlmAgent(
    name="user_understanding_agent",
    model=MODEL,
    description="It's work is to greet the user and understand the user very well emotionally, characterically very well before starting the startup journey.",
    instruction=prompt.USER_UNDERSTANDING_PROMPT,
    tools=[
        collect_user_name_tool,
        collect_user_age_tool,
        collect_user_location_tool,
        collect_user_background_tool,
        collect_financial_condition_tool,
        collect_responsibilities_tool,
        collect_startup_dream_tool,
        collect_challenges_tool,
        collect_available_time_tool,
    ],
    output_key="user_understanding"
)
