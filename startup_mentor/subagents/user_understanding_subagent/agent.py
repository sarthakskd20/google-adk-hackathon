from google.adk.tools import FunctionTool
from google.adk.tools.tool_context import ToolContext
from google.adk.agents import LlmAgent
from . import prompt

MODEL = "gemini-2.0-flash"

# Required fields to check for completion
REQUIRED_FIELDS = {
    "user_name": "",
    "user_age": "",
    "user_location": "",
    "user_background": "",
    "user_financial_background": "",
    "user_responsibilities": "",
    "user_startup_dream": "",
    "user_available_time": "",
    "user_challenges": "",
}

def validate_response(collected_value: str) -> bool:
    """Validate if the collected value is satisfactory."""
    return collected_value is not None and str(collected_value).strip() != ""

# --- 1. User Name ---
def collect_user_name(user_input: str, tool_context: ToolContext) -> dict:
    """Collect and validate the user's name."""
    name = user_input.strip().title()
    if not validate_response(name):
        return {
            "status": "incomplete",
            "message": "Please provide your name."
        }
    
    tool_context.state["user_name"] = name
    return {
        "status": "success",
        "action": "collect_user_name",
        "collected_value": name,
        "message": "USER_NAME_COLLECTED"
    }

# --- 2. Age ---
def collect_user_age(user_input: str, tool_context: ToolContext) -> dict:
    """Collect and validate the user's age."""
    age = user_input.strip()
    if not validate_response(age):
        return {
            "status": "incomplete",
            "message": "Please provide your age."
        }
    
    tool_context.state["user_age"] = age
    return {
        "status": "success",
        "action": "collect_user_age",
        "collected_value": age,
        "message": "AGE_COLLECTED"
    }

# --- 3. Location ---
def collect_user_location(user_input: str, tool_context: ToolContext) -> dict:
    """Collect and validate the user's location."""
    location = user_input.strip()
    if not validate_response(location):
        return {
            "status": "incomplete",
            "message": "Please provide your location."
        }
    
    tool_context.state["user_location"] = location
    return {
        "status": "success",
        "action": "collect_user_location",
        "collected_value": location,
        "message": "LOCATION_COLLECTED"
    }

# --- 4. Background ---
def collect_user_background(user_input: str, tool_context: ToolContext) -> dict:
    """Collect and validate the user's background information."""
    background = user_input.strip()
    if not validate_response(background):
        return {
            "status": "incomplete",
            "message": "Please provide your background information."
        }
    
    tool_context.state["user_background"] = background
    return {
        "status": "success",
        "action": "collect_user_background",
        "collected_value": background,
        "message": "BACKGROUND_COLLECTED"
    }

# --- 5. Financial Situation ---
def collect_financial_condition(user_input: str, tool_context: ToolContext) -> dict:
    """Collect and validate the user's financial situation."""
    financial_info = user_input.strip()
    if not validate_response(financial_info):
        return {
            "status": "incomplete",
            "message": "Please provide information about your financial situation."
        }
    
    tool_context.state["user_financial_background"] = financial_info
    return {
        "status": "success",
        "action": "collect_financial_condition",
        "collected_value": financial_info,
        "message": "FINANCIAL_BACKGROUND_COLLECTED"
    }

# --- 6. Responsibilities ---
def collect_responsibilities(user_input: str, tool_context: ToolContext) -> dict:
    """Collect and validate the user's responsibilities."""
    responsibilities = user_input.strip()
    if not validate_response(responsibilities):
        return {
            "status": "incomplete",
            "message": "Please provide information about your responsibilities."
        }
    
    tool_context.state["user_responsibilities"] = responsibilities
    return {
        "status": "success",
        "action": "collect_responsibilities",
        "collected_value": responsibilities,
        "message": "RESPONSIBILITIES_COLLECTED"
    }

# --- 7. Startup Idea ---
def collect_startup_dream(user_input: str, tool_context: ToolContext) -> dict:
    """Collect and validate the user's startup idea."""
    startup_dream = user_input.strip()
    if not validate_response(startup_dream):
        return {
            "status": "incomplete",
            "message": "Please share your startup idea or ambition."
        }
    
    tool_context.state["user_startup_dream"] = startup_dream
    return {
        "status": "success",
        "action": "collect_startup_dream",
        "collected_value": startup_dream,
        "message": "STARTUP_DREAM_COLLECTED"
    }

# --- 8. Time Commitment ---
def collect_available_time(user_input: str, tool_context: ToolContext) -> dict:
    """Collect and validate the user's available time commitment."""
    available_time = user_input.strip()
    if not validate_response(available_time):
        return {
            "status": "incomplete",
            "message": "Please provide information about your available time commitment."
        }
    
    tool_context.state["user_available_time"] = available_time
    return {
        "status": "success",
        "action": "collect_available_time",
        "collected_value": available_time,
        "message": "TIME_AVAILABLE_COLLECTED"
    }

# --- 9. Challenges ---
def collect_challenges(user_input: str, tool_context: ToolContext) -> dict:
    """Collect and validate the user's challenges."""
    challenges = user_input.strip()
    if not validate_response(challenges):
        return {
            "status": "incomplete",
            "message": "Please share any challenges you're facing."
        }
    
    tool_context.state["user_challenges"] = challenges
    return {
        "status": "success",
        "action": "collect_challenges",
        "collected_value": challenges,
        "message": "CHALLENGES_COLLECTED"
    }

def check_completion(tool_context: ToolContext) -> bool:
    """Check if all required fields have been completed."""
    for field in REQUIRED_FIELDS:
        if field not in tool_context.state or not validate_response(tool_context.state.get(field, "")):
            return False
    return True

def get_missing_fields(tool_context: ToolContext) -> list:
    """Get a list of fields that are missing or incomplete."""
    missing_fields = []
    for field in REQUIRED_FIELDS:
        if field not in tool_context.state or not validate_response(tool_context.state.get(field, "")):
            missing_fields.append(field)
    return missing_fields

# --- Create Tool Instances ---
collect_user_name_tool = FunctionTool(func=collect_user_name)
collect_user_age_tool = FunctionTool(func=collect_user_age)
collect_user_location_tool = FunctionTool(func=collect_user_location)
collect_user_background_tool = FunctionTool(func=collect_user_background)
collect_financial_condition_tool = FunctionTool(func=collect_financial_condition)
collect_responsibilities_tool = FunctionTool(func=collect_responsibilities)
collect_startup_dream_tool = FunctionTool(func=collect_startup_dream)
collect_available_time_tool = FunctionTool(func=collect_available_time)
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
