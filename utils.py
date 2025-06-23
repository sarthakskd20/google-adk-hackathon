from datetime import datetime
from google.genai import types
from typing import Dict, Any, Optional, Tuple
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
APP_NAME = "DreamWeaver AI"

# ANSI color codes for terminal output
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BG_BLUE = "\033[44m"
    BG_RED = "\033[41m"
    BG_WHITE = "\033[47m"

def format_state_field(value: Any, default: str = 'Not specified') -> str:
    """Format a state field value for display."""
    if value is None:
        return default
    if isinstance(value, str) and not value.strip():
        return default
    return str(value)

def display_state(session_state: Dict[str, Any], label: str = "Current State") -> None:
    """Display the current session state in a formatted way."""
    try:
        # Format the output with clear sections
        print(f"\n{'-' * 10} {label} {'-' * 10}")

        # Display user profile information
        print("👤 User Profile:")
        print(f"  • Name: {format_state_field(session_state.get('user_name'))}")
        print(f"  • Age: {format_state_field(session_state.get('user_age'))}")
        print(f"  • Location: {format_state_field(session_state.get('user_location'))}")
        print(f"  • Background: {format_state_field(session_state.get('user_background'))}")
        print(f"  • Financial Background: {format_state_field(session_state.get('user_financial_background'))}")
        print(f"  • Responsibilities: {format_state_field(session_state.get('user_responsibilities'))}")
        
        print("\n🎯 Startup Dreams:")
        print(f"  • Startup Dream: {format_state_field(session_state.get('user_startup_dream'))}")
        
        # Display availability and challenges
        print("\n⏰ Availability & Challenges:")
        print(f"  • Available Time: {format_state_field(session_state.get('user_available_time'))}")
        print(f"  • Challenges: {format_state_field(session_state.get('user_challenges'))}")
        
        print(f"\n{'=' * 30}\n")
    except Exception as e:
        logger.error(f"Error displaying state: {e}")
        print(f"{Colors.RED}Error displaying state: {e}{Colors.RESET}")

async def process_agent_response(event) -> Optional[str]:
    """Process and display agent response events."""
    final_response = None
    
    try:
        # Skip processing if it's a system event
        if event.author == "system":
            return None

        # Log basic event info
        logger.debug(f"Processing event from {event.author}")

        # Process all parts of the event
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "executable_code") and part.executable_code:
                    logger.debug(f"Agent generated code: {part.executable_code.code}")
                elif hasattr(part, "code_execution_result") and part.code_execution_result:
                    logger.debug(f"Code Execution Result: {part.code_execution_result.outcome}")
                elif hasattr(part, "tool_response") and part.tool_response:
                    logger.debug(f"Tool Response: {part.tool_response.output}")
                elif hasattr(part, "text") and part.text and part.text.strip():
                    if event.is_final_response():
                        final_response = part.text.strip()
                        logger.info(f"Final response from {event.author}: {final_response}")
                    else:
                        logger.info(f"Intermediate response: {part.text.strip()}")

        # Special formatting for final response
        if event.is_final_response():
            if final_response:
                print(f"\n{Colors.CYAN}{Colors.BOLD}=== AGENT RESPONSE ==={Colors.RESET}")
                print(f"{final_response}")
                print(f"{Colors.CYAN}{Colors.BOLD}====================={Colors.RESET}\n")
            else:
                logger.warning("Final response event had no text content")

    except Exception as e:
        logger.error(f"Error processing agent response: {e}")
        print(f"{Colors.RED}Error processing agent response: {e}{Colors.RESET}")
    
    return final_response

async def call_agent_async(runner, user_id: str, session_id: str, query: str) -> Tuple[Optional[str], Dict[str, Any]]:
    """Execute an agent call asynchronously and return the final response and state."""
    content = types.Content(role="user", parts=[types.Part(text=query)])
    final_response_text = None
    session_state = {}
    
    logger.info(f"Running query: {query}")
    
    try:
        # Get session
        session = runner.session_service.get_session(
            app_name=runner.app_name,
            user_id=user_id,
            session_id=session_id
        )
        
        # Process agent events
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content
        ):
            response = await process_agent_response(event)
            if response:
                final_response_text = response
        
        # Get updated state
        session = runner.session_service.get_session(
            app_name=runner.app_name,
            user_id=user_id,
            session_id=session_id
        )
        session_state = session.state.copy()
        
        # Log missing fields if any
        missing_fields = get_missing_profile_fields(session_state)
        if missing_fields:
            logger.info(f"Still missing fields: {missing_fields}")
        
    except Exception as e:
        logger.error(f"Error during agent call: {e}")
    
    return final_response_text, session_state

def is_user_profile_complete(state: Dict[str, Any]) -> bool:
    """Check if all required profile fields are filled."""
    required_fields = [
        "user_name",
        "user_age",
        "user_location",
        "user_background",
        "user_financial_background",
        "user_responsibilities",
        "user_startup_dream",
        "user_challenges",
        "user_available_time",
    ]
    
    # Detailed check with logging
    missing_fields = [field for field in required_fields if not state.get(field)]
    if missing_fields:
        logger.info(f"Missing profile fields: {missing_fields}")
        return False
    return True

def get_missing_profile_fields(state: Dict[str, Any]) -> list:
    """Get a list of missing required profile fields."""
    required_fields = [
        "user_name",
        "user_age",
        "user_location",
        "user_background",
        "user_financial_background",
        "user_responsibilities",
        "user_startup_dream",
        "user_available_time",
        "user_challenges",
    ]
    return [field for field in required_fields if not state.get(field)]
