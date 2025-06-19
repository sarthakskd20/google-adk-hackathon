import asyncio
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from datetime import datetime
from typing import Dict, List
import threading

# Import the main customer service agent
from startup_mentor.agent import startup_mentor
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from utils import add_user_query_to_history, call_agent_async, add_agent_response_to_history

load_dotenv()

class ModernChatUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Startup Mentor")
        self.sessions: Dict[str, List[dict]] = {}
        self.current_session = None
        self.current_backend_session = None
        self.running = True
        
        # Modern color scheme (dark mode)
        self.bg_color = "#343541"
        self.header_color = "#202123"
        self.user_msg_color = "#444654"
        self.agent_msg_color = "#343541"
        self.text_color = "#ECECF1"
        self.accent_color = "#10A37F"
        self.input_bg = "#40414F"
        self.button_color = "#10A37F"
        
        # Configure window
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        self.root.configure(bg=self.bg_color)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Custom window styling
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.header_color, foreground=self.text_color)
        self.style.configure('TButton', 
                           background=self.button_color, 
                           foreground="white",
                           borderwidth=0,
                           focuscolor=self.button_color,
                           font=('Segoe UI', 10))
        self.style.map('TButton',
                      background=[('active', self.accent_color), ('pressed', self.accent_color)])
        
        # Create main frames with modern styling
        self.header_frame = ttk.Frame(self.root, height=60, style='TFrame')
        self.header_frame.pack(fill=tk.X, padx=0, pady=0)
        
        self.chat_frame = ttk.Frame(self.root, style='TFrame')
        self.chat_frame.pack(expand=True, fill=tk.BOTH, padx=0, pady=0)
        
        self.input_frame = ttk.Frame(self.root, height=120, style='TFrame')
        self.input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Header widgets with modern look
        self.logo_label = ttk.Label(
            self.header_frame,
            text="Startup Mentor",
            font=('Segoe UI', 14, 'bold'),
            style='TLabel'
        )
        self.logo_label.pack(side=tk.LEFT, padx=20)
        
        self.session_label = ttk.Label(
            self.header_frame,
            text="New Chat",
            font=('Segoe UI', 10),
            style='TLabel'
        )
        self.session_label.pack(side=tk.LEFT, padx=10)
        
        self.new_session_btn = ttk.Button(
            self.header_frame,
            text="+ New Chat",
            command=self.create_new_session,
            style='TButton'
        )
        self.new_session_btn.pack(side=tk.RIGHT, padx=20)
        
        # Chat display with modern styling
        self.chat_display = scrolledtext.ScrolledText(
            self.chat_frame,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=('Segoe UI', 12),
            bg=self.bg_color,
            fg=self.text_color,
            insertbackground=self.text_color,
            padx=20,
            pady=20,
            borderwidth=0,
            highlightthickness=0
        )
        self.chat_display.pack(expand=True, fill=tk.BOTH)
        
        # Custom tags for message styling
        self.chat_display.tag_config("user", 
                                   background=self.user_msg_color,
                                   lmargin1=20,
                                   lmargin2=20,
                                   rmargin=20,
                                   spacing3=10)
        self.chat_display.tag_config("agent", 
                                   background=self.agent_msg_color,
                                   lmargin1=20,
                                   lmargin2=20,
                                   rmargin=20,
                                   spacing3=10)
        self.chat_display.tag_config("system", 
                                   foreground="#888",
                                   font=('Segoe UI', 10, 'italic'))
        self.chat_display.tag_config("timestamp", 
                                   foreground="#888",
                                   font=('Segoe UI', 8))
        
        # Modern input area
        self.input_container = ttk.Frame(self.input_frame, style='TFrame')
        self.input_container.pack(fill=tk.BOTH, expand=True)
        
        self.input_entry = tk.Text(
            self.input_container,
            height=3,
            wrap=tk.WORD,
            font=('Segoe UI', 12),
            bg=self.input_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            padx=15,
            pady=15,
            borderwidth=0,
            highlightthickness=0,
            relief=tk.FLAT
        )
        self.input_entry.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        # Send button with modern style
        self.send_btn = ttk.Button(
            self.input_container,
            text="➤",  # Using arrow character instead of "Send"
            command=self.send_message,
            style='TButton',
            width=3
        )
        self.send_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Bind Enter key (with Shift for new line)
        self.input_entry.bind("<Return>", self.on_enter_pressed)
        
        # Asyncio setup
        self.loop = asyncio.new_event_loop()
        self.task = None
        
        # Add some visual polish
        self.create_gradient_header()
        self.add_scrollbar_style()
    
    def create_gradient_header(self):
        """Create a subtle gradient effect for the header"""
        canvas = tk.Canvas(self.header_frame, 
                          height=60, 
                          bg=self.header_color,
                          highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # Draw gradient (simple version - can be enhanced)
        for i in range(60):
            color = self.interpolate_color(self.header_color, "#2b2d3a", i/60)
            canvas.create_line(0, i, 2000, i, fill=color)
        
        # Place widgets on top of canvas
        self.logo_label.lift()
        self.session_label.lift()
        self.new_session_btn.lift()
    
    def interpolate_color(self, color1, color2, ratio):
        """Helper function to interpolate between two colors"""
        # Convert hex to RGB
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        
        # Interpolate
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        
        # Convert back to hex
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def add_scrollbar_style(self):
        """Customize scrollbar appearance"""
        self.style.configure("Vertical.TScrollbar",
                           background=self.bg_color,
                           troughcolor=self.bg_color,
                           bordercolor=self.bg_color,
                           arrowcolor=self.text_color,
                           gripcount=0)
        
        # Apply to chat display
        self.chat_display.configure(yscrollcommand=lambda *args: self.chat_display.yview(*args))
        
    def on_close(self):
        """Handle window close"""
        self.running = False
        if self.task:
            self.task.cancel()
        self.root.quit()
    
    def create_new_session(self):
        """Handle new session creation with modern dialog"""
        if self.current_backend_session:
            response = messagebox.askyesno(
                "New Chat",
                "Start a new chat? Current conversation will be saved but hidden.",
                parent=self.root
            )
            if not response:
                return
        
        new_session = session_service.create_session(
            app_name="Startup Mentor",
            user_id="28475935",
            state=initial_state,
        )
        self.current_backend_session = new_session
        self.create_session(new_session.id)
        self.add_message("system", "New chat started. How can I help you today?")
    
    def create_session(self, session_id: str):
        """Create a new chat session"""
        self.sessions[session_id] = []
        self.current_session = session_id
        self.update_session_header()
    
    def update_session_header(self):
        """Update the session info in header"""
        session_display = "New Chat" if not self.current_session else f"Chat: {self.current_session[:8]}"
        self.session_label.config(text=session_display)
    
    def add_message(self, role: str, content: str):
        """Add a message to the current session with modern styling"""
        if not self.current_session or not self.running:
            return
            
        timestamp = datetime.now().strftime("%H:%M")
        
        # Add avatar and proper alignment based on role
        if role == "user":
            avatar = "👤"
            tag = "user"
            indent = ""
        elif role == "agent":
            avatar = "🤖"
            tag = "agent"
            indent = "  "
        else:
            avatar = "⚙️"
            tag = "system"
            indent = ""
        
        # Display message in chat with modern formatting
        try:
            self.chat_display.config(state=tk.NORMAL)
            
            # Add avatar and timestamp
            self.chat_display.insert(tk.END, f"{avatar} ", tag)
            self.chat_display.insert(tk.END, f"[{timestamp}]\n", "timestamp")
            
            # Add message content with proper indentation
            lines = content.split('\n')
            for line in lines:
                self.chat_display.insert(tk.END, f"{indent}{line}\n", tag)
            
            # Add separator
            self.chat_display.insert(tk.END, "\n", tag)
            
            self.chat_display.config(state=tk.DISABLED)
            self.chat_display.see(tk.END)
        except tk.TclError:
            pass
    
    def send_message(self):
        """Handle sending a message with visual feedback"""
        input_text = self.input_entry.get("1.0", tk.END).strip()
        if not input_text:
            return
            
        # Clear input and temporarily disable
        self.input_entry.delete("1.0", tk.END)
        self.input_entry.config(state=tk.DISABLED)
        self.send_btn.config(state=tk.DISABLED)
        
        # Visual feedback
        self.add_message("user", input_text)
        
        # Run the async task
        asyncio.run_coroutine_threadsafe(
            self.handle_user_input(input_text),
            self.loop
        )
    
    def on_enter_pressed(self, event):
        """Handle Enter key press (without Shift creates new line)"""
        if not event.state & 0x1:  # If Shift not held
            self.send_message()
            return "break"
        return None
    
    async def handle_user_input(self, input_text):
        """Process user input and get agent response"""
        if not self.running:
            return
            
        if input_text.lower() in ["/exit", "exit"]:
            self.on_close()
            return
            
        # Add to history
        add_user_query_to_history(
            session_service, 
            "Startup Mentor", 
            "28475935", 
            self.current_backend_session.id, 
            input_text
        )
        
        # Get agent response
        try:
            response, agent_name = await call_agent_async(
                runner, 
                "28475935", 
                self.current_backend_session.id, 
                input_text
            )
            self.add_message("agent", response)
            
            # Add to history
            add_agent_response_to_history(
                session_service,
                "Startup Mentor",
                "28475935",
                self.current_backend_session.id,
                agent_name,
                response
            )
        except Exception as e:
            self.add_message("system", f"Error: {str(e)}")
        finally:
            # Re-enable input
            self.root.after(0, lambda: [
                self.input_entry.config(state=tk.NORMAL),
                self.send_btn.config(state=tk.NORMAL),
                self.input_entry.focus()
            ])

# ===== Initialize services =====
session_service = InMemorySessionService()
initial_state = {
    "user_name": "Brandon Hancock",
    "purchased_courses": [],
    "interaction_history": [],
}

def main():
    """Entry point for the application."""
    try:
        # Initialize components
        new_session = session_service.create_session(
            app_name="Startup Mentor",
            user_id="28475935",
            state=initial_state,
        )
        global runner
        runner = Runner(
            agent=startup_mentor,
            app_name="Startup Mentor",
            session_service=session_service,
        )
        
        # Create Tkinter UI
        root = tk.Tk()
        
        # Set window icon if available
        try:
            root.iconbitmap('icon.ico')  # Replace with your icon file
        except:
            pass
        
        ui = ModernChatUI(root)
        ui.current_backend_session = new_session
        ui.create_session(new_session.id)
        ui.add_message("system", "Welcome to Startup Mentor! How can I help you today?")
        
        # Run the asyncio event loop in a separate thread
        def run_asyncio_loop(loop):
            asyncio.set_event_loop(loop)
            loop.run_forever()
        
        asyncio_thread = threading.Thread(
            target=run_asyncio_loop,
            args=(ui.loop,),
            daemon=True
        )
        asyncio_thread.start()
        
        # Run the Tkinter mainloop
        root.mainloop()
        
        # Cleanup when mainloop ends
        ui.loop.call_soon_threadsafe(ui.loop.stop)
        asyncio_thread.join()
        
    except KeyboardInterrupt:
        print("\nApplication terminated by user")

if __name__ == "__main__":
    main()