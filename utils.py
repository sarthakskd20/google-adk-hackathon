from datetime import datetime
from google.genai import types
from typing import Dict, Any

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

# --- Display Session State ---
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
        
        # Display goals and dreams
        print("\n🎯 Goals & Dreams:")
        print(f"  • Goals: {format_state_field(session_state.get('user_goals'))}")
        print(f"  • Startup Dream: {format_state_field(session_state.get('user_startup_dream'))}")
        
        # Display availability and challenges
        print("\n⏰ Availability & Challenges:")
        print(f"  • Available Time: {format_state_field(session_state.get('user_available_time'))}")
        print(f"  • Challenges: {format_state_field(session_state.get('user_challenges'))}")
        print(f"  • Mindset: {format_state_field(session_state.get('user_mindset'))}")
        
        print(f"\n{'=' * 30}\n")
    except Exception as e:
        print(f"{Colors.RED}Error displaying state: {e}{Colors.RESET}")

# --- Async Call and Agent Event Processing ---
async def process_agent_response(event) -> str:
    """Process and display agent response events."""
    final_response = None
    
    try:
        # Log basic event info
        print(f"{Colors.MAGENTA}Event ID: {event.id}, Author: {event.author}{Colors.RESET}")

        # Process all parts of the event
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "executable_code") and part.executable_code:
                    print(
                        f"{Colors.YELLOW}  Debug: Agent generated code:\n```python\n{part.executable_code.code}\n```{Colors.RESET}"
                    )
                elif hasattr(part, "code_execution_result") and part.code_execution_result:
                    print(
                        f"{Colors.YELLOW}  Debug: Code Execution Result: {part.code_execution_result.outcome} - Output:\n{part.code_execution_result.output}{Colors.RESET}"
                    )
                elif hasattr(part, "tool_response") and part.tool_response:
                    print(f"{Colors.BLUE}  Tool Response: {part.tool_response.output}{Colors.RESET}")
                elif hasattr(part, "text") and part.text and part.text.strip():
                    print(f"{Colors.GREEN}  Text: '{part.text.strip()}'{Colors.RESET}")
                    if event.is_final_response():
                        final_response = part.text.strip()

        # Special formatting for final response
        if event.is_final_response() and final_response:
            print(
                f"\n{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}╔══ AGENT RESPONSE ═════════════════════════════════════════{Colors.RESET}"
            )
            print(f"{Colors.CYAN}{Colors.BOLD}{final_response}{Colors.RESET}")
            print(
                f"{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}╚═════════════════════════════════════════════════════════════{Colors.RESET}\n"
            )
        elif event.is_final_response() and not final_response:
            print(
                f"\n{Colors.BG_RED}{Colors.WHITE}{Colors.BOLD}==> Final Agent Response: [No text content in final event]{Colors.RESET}\n"
            )

    except Exception as e:
        print(f"{Colors.RED}Error processing agent response: {e}{Colors.RESET}")
    
    return final_response

async def call_agent_async(runner, user_id: str, session_id: str, query: str) -> tuple:
    """Execute an agent call asynchronously and return the final response."""
    content = types.Content(role="user", parts=[types.Part(text=query)])
    final_response_text = None
    
    print(
        f"\n{Colors.BG_BLUE}{Colors.BLACK}{Colors.BOLD}--- Running Query: {query} ---{Colors.RESET}"
    )
    
    try:
        # Get initial state
        session = runner.session_service.get_session(
            app_name=runner.app_name,
            user_id=user_id,
            session_id=session_id
        )
        display_state(session.state, "State BEFORE processing")
        
        # Create a list to collect all events
        events = []
        
        # Process agent events
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content
        ):
            events.append(event)  # Collect all events
            response = await process_agent_response(event)
            if response:
                final_response_text = response
        
        # After processing all events, force a session refresh
        session = runner.session_service.get_session(
            app_name=runner.app_name,
            user_id=user_id,
            session_id=session_id,
            # force_refresh=True  # Ensure we get the latest state
        )
        
        # Debug: Print raw state to see what's actually there
        print(f"\n{Colors.YELLOW}DEBUG - Raw State:{Colors.RESET}")
        for key, value in session.state.items():
            print(f"{key}: {value}")
        
        display_state(session.state, "State AFTER processing")
        
    except Exception as e:
        print(f"{Colors.RED}Error during agent call: {e}{Colors.RESET}")
    
    return final_response_text, None

# --- Profile Completion Checker ---
def is_user_profile_complete(state: Dict[str, Any]) -> bool:
    """Check if all required profile fields are filled."""
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
