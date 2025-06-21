import asyncio
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from datetime import datetime
from typing import Dict, List
import threading
import webbrowser
from PIL import Image, ImageTk
import sv_ttk  # Modern theme for tkinter

# Import the main customer service agent
from startup_mentor.agent import startup_mentor_orchestrator
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from utils import call_agent_async, get_missing_profile_fields

load_dotenv()

class ModernChatUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Startup Mentor AI")
        self.sessions: Dict[str, List[dict]] = {}
        self.current_session = None
        self.current_backend_session = None
        self.running = True
        
        # Modern color scheme (dark mode)
        self.bg_color = "#181825"  # Darker slate
        self.header_color = "#181825"  # Darker slate
        self.user_msg_color = "#585b70"  # Muted lavender
        self.agent_msg_color = "#313244"  # Dark slate
        self.text_color = "#cdd6f4"  # Light text
        self.accent_color = "#89b4fa"  # Soft blue
        self.input_bg = "#45475a"  # Light slate
        self.button_color = "#89b4fa"  # Soft blue
        self.button_hover = "#74c7ec"  # Lighter blue
        self.error_color = "#f38ba8"  # Soft red
        self.success_color = "#a6e3a1"  # Soft green
        
        # Configure window
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        self.root.configure(bg=self.bg_color)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Apply modern theme
        sv_ttk.set_theme("dark")
        
        # Custom window styling
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.header_color, foreground=self.text_color, font=('Segoe UI', 10))
        self.style.configure('TButton', 
                           background=self.button_color,
                           foreground="#1e1e1e",
                           borderwidth=0,
                           focuscolor=self.button_color,
                           font=('Segoe UI', 10, 'bold'),
                           padding=8)
        self.style.map('TButton',
                      background=[('active', self.button_hover), ('pressed', self.button_hover)])
        
        # Create main frames with modern styling
        self.header_frame = ttk.Frame(self.root, height=70, style='TFrame')
        self.header_frame.pack(fill=tk.X, padx=0, pady=0)
        
        # Sidebar for session history
        self.sidebar_frame = ttk.Frame(self.root, width=250, style='TFrame')
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        self.sidebar_frame.pack_propagate(False)
        
        self.chat_frame = ttk.Frame(self.root, style='TFrame')
        self.chat_frame.pack(expand=True, fill=tk.BOTH, padx=0, pady=0)
        
        self.input_frame = ttk.Frame(self.root, height=150, style='TFrame')
        self.input_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Header widgets with modern look
        self.logo_frame = ttk.Frame(self.header_frame, style='TFrame')
        self.logo_frame.pack(side=tk.LEFT, padx=20)
        
        try:
            # Try to load a logo image
            self.logo_img = Image.open("logo.png").resize((40, 40))
            self.logo_photo = ImageTk.PhotoImage(self.logo_img)
            self.logo_label = ttk.Label(self.logo_frame, image=self.logo_photo, background=self.header_color)
            self.logo_label.pack(side=tk.LEFT)
        except:
            # Fallback to text logo
            self.logo_label = ttk.Label(
                self.logo_frame,
                text="🚀",
                font=('Segoe UI', 24),
                style='TLabel'
            )
            self.logo_label.pack(side=tk.LEFT, padx=5)
        
        self.title_label = ttk.Label(
            self.logo_frame,
            text="Startup Mentor AI",
            font=('Segoe UI', 16, 'bold'),
            style='TLabel'
        )
        self.title_label.pack(side=tk.LEFT, padx=10)
        
        self.session_label = ttk.Label(
            self.header_frame,
            text="New Chat",
            font=('Segoe UI', 10),
            style='TLabel'
        )
        self.session_label.pack(side=tk.LEFT, padx=10, expand=True)
        
        # Header buttons
        self.button_frame = ttk.Frame(self.header_frame, style='TFrame')
        self.button_frame.pack(side=tk.RIGHT, padx=10)
        
        self.new_session_btn = ttk.Button(
            self.button_frame,
            text="New Chat",
            command=self.create_new_session,
            style='TButton'
        )
        self.new_session_btn.pack(side=tk.LEFT, padx=5)
        
        self.settings_btn = ttk.Button(
            self.button_frame,
            text="⚙️",
            command=self.show_settings,
            style='TButton',
            width=3
        )
        self.settings_btn.pack(side=tk.LEFT, padx=5)
        # Modern sidebar content with cards for each chat
        self.sidebar_title_frame = ttk.Frame(self.sidebar_frame, style='TFrame')
        self.sidebar_title_frame.pack(fill=tk.X, padx=10, pady=(15, 10))
        
        self.sidebar_title = ttk.Label(
            self.sidebar_title_frame,
            text="Chat History",
            font=('Segoe UI', 12, 'bold'),
            style='TLabel'
        )
        self.sidebar_title.pack(side=tk.LEFT)
        
        
        # Sidebar content
        self.sidebar_title = ttk.Label(
            self.sidebar_frame,
            text="Chat History",
            font=('Segoe UI', 12, 'bold'),
            style='TLabel'
        )
        self.sidebar_title.pack(pady=(15, 10), padx=10, anchor='w')
        
        self.session_list = tk.Listbox(
            self.sidebar_frame,
            bg=self.input_bg,
            fg=self.text_color,
            selectbackground=self.accent_color,
            selectforeground="#1e1e1e",
            font=('Segoe UI', 10),
            borderwidth=0,
            highlightthickness=0,
            activestyle='none'
        )
        self.session_list.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)
        self.session_list.bind('<<ListboxSelect>>', self.load_session)
        
        self.sidebar_footer = ttk.Frame(self.sidebar_frame, style='TFrame')
        self.sidebar_footer.pack(fill=tk.X, padx=10, pady=10)
        
        self.help_btn = ttk.Button(
            self.sidebar_footer,
            text="Help & FAQ",
            command=self.open_help,
            style='TButton'
        )
        self.help_btn.pack(fill=tk.X, pady=5)
        
        # Chat display with modern styling
        self.chat_container = ttk.Frame(self.chat_frame, style='TFrame')
        self.chat_container.pack(expand=True, fill=tk.BOTH, padx=0, pady=0)
        
        self.chat_display = scrolledtext.ScrolledText(
            self.chat_container,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=('Segoe UI', 12),
            bg=self.bg_color,
            fg=self.text_color,
            insertbackground=self.text_color,
            padx=20,
            pady=20,
            borderwidth=0,
            highlightthickness=0,
            relief=tk.FLAT
        )
        self.chat_display.pack(expand=True, fill=tk.BOTH)
        
        # Custom tags for message styling with modern look
        self.chat_display.tag_config("user", 
                                   background=self.user_msg_color,
                                   lmargin1=20,
                                   lmargin2=20,
                                   rmargin=20,
                                   spacing3=10,
                                   borderwidth=0,
                                   relief=tk.FLAT,
                                   wrap=tk.WORD)
        self.chat_display.tag_config("agent", 
                                   background=self.agent_msg_color,
                                   lmargin1=20,
                                   lmargin2=20,
                                   rmargin=20,
                                   spacing3=10,
                                   borderwidth=0,
                                   relief=tk.FLAT,
                                   wrap=tk.WORD)
        self.chat_display.tag_config("system", 
                                   foreground="#a6adc8",
                                   font=('Segoe UI', 10, 'italic'))
        self.chat_display.tag_config("timestamp", 
                                   foreground="#7f849c",
                                   font=('Segoe UI', 8))
        self.chat_display.tag_config("thinking", 
                                   foreground="#a6adc8",
                                   font=('Segoe UI', 10, 'italic'))
        # Status bar
        self.status_bar = ttk.Frame(self.chat_container, height=25, style='TFrame')
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_label = ttk.Label(
            self.status_bar,
            text="Ready",
            font=('Segoe UI', 8),
            style='TLabel'
        )
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Modern input area with rounded corners
        self.input_container = ttk.Frame(self.input_frame, style='TFrame')
        self.input_container.pack(fill=tk.BOTH, expand=True)
        
        self.input_entry = tk.Text(
            self.input_container,
            height=4,
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
        self.input_entry.bind("<KeyRelease>", self.update_send_button_state)
        
        # Button container
        self.button_container = ttk.Frame(self.input_container, width=80, style='TFrame')
        self.button_container.pack(side=tk.RIGHT, fill=tk.Y)
        self.button_container.pack_propagate(False)
        
        # Send button with modern style
        self.send_btn = ttk.Button(
            self.button_container,
            text="Send",
            command=self.send_message,
            style='TButton',
            state=tk.DISABLED
        )
        self.send_btn.pack(fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Additional action buttons
        self.action_btn_frame = ttk.Frame(self.button_container, style='TFrame')
        self.action_btn_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.clear_btn = ttk.Button(
            self.action_btn_frame,
            text="🗑️",
            command=self.clear_input,
            style='TButton',
            width=3
        )
        self.clear_btn.pack(side=tk.LEFT, expand=True)
        
        # Bind Enter key (with Shift for new line)
        self.input_entry.bind("<Return>", self.on_enter_pressed)
        
        # Tooltip system
        self.tooltip_window = None
        
        # Asyncio setup
        self.loop = asyncio.new_event_loop()
        self.task = None
        
        # Add typing indicator
        self.typing_indicator = None
        
        # Add some visual polish
        self.create_gradient_header()
        self.style_scrollbars()
        
        # Focus on input field
        self.input_entry.focus_set()
    
    def style_scrollbars(self):
        """Custom scrollbar styling"""
        self.style.configure("Vertical.TScrollbar", 
                           background=self.bg_color,
                           troughcolor=self.bg_color,
                           bordercolor=self.bg_color,
                           arrowcolor=self.text_color,
                           gripcount=0)
        
        scrollbar = ttk.Scrollbar(self.chat_container, style="Vertical.TScrollbar")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_display.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.chat_display.yview)
    
    def create_gradient_header(self):
        """Create a subtle gradient effect for the header"""
        canvas = tk.Canvas(self.header_frame, 
                          height=70, 
                          bg=self.header_color,
                          highlightthickness=0,
                          bd=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # Draw gradient (simple version - can be enhanced)
        for i in range(70):
            color = self.interpolate_color(self.header_color, "#1a1a24", i/70)
            canvas.create_line(0, i, 2000, i, fill=color)
        
        # Place widgets on top of canvas
        self.logo_frame.lift()
        self.session_label.lift()
        self.button_frame.lift()
    
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
    
    def update_send_button_state(self, event=None):
        """Enable/disable send button based on input content"""
        if self.input_entry.get("1.0", "end-1c").strip():
            self.send_btn.config(state=tk.NORMAL)
        else:
            self.send_btn.config(state=tk.DISABLED)
    
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
        self.session_list.insert(tk.END, f"Chat {len(self.sessions)}")
        self.session_list.selection_clear(0, tk.END)
        self.session_list.selection_set(tk.END)
        self.update_session_header()
    
    def load_session(self, event):
        """Load a previous session"""
        selection = self.session_list.curselection()
        if selection:
            session_index = selection[0]
            # In a real app, you would load the session data here
            self.update_session_header(f"Loaded chat {session_index + 1}")
    
    def update_session_header(self, text=None):
        """Update the session info in header"""
        if text is None:
            session_display = "New Chat" if not self.current_session else f"Chat: {self.current_session[:8]}"
        else:
            session_display = text
        self.session_label.config(text=session_display)
    
    def show_typing_indicator(self):
        """Show that the agent is typing"""
        if self.typing_indicator:
            self.chat_display.delete(self.typing_indicator)
        
        self.chat_display.config(state=tk.NORMAL)
        self.typing_indicator = self.chat_display.insert(
            tk.END, "Startup Mentor is typing...\n\n", "thinking"
        )
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def hide_typing_indicator(self):
        """Remove the typing indicator"""
        if self.typing_indicator:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete(self.typing_indicator)
            self.typing_indicator = None
            self.chat_display.config(state=tk.DISABLED)
    
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
    
    def clear_input(self):
        """Clear the input field"""
        self.input_entry.delete("1.0", tk.END)
        self.update_send_button_state()
    
    def send_message(self):
        """Handle sending a message with visual feedback"""
        user_input = self.input_entry.get("1.0", tk.END).strip()
        if not user_input:
            return
            
        # Clear input and temporarily disable
        self.clear_input()
        self.input_entry.config(state=tk.DISABLED)
        self.send_btn.config(state=tk.DISABLED)
        
        # Visual feedback
        self.add_message("user", user_input)
        self.show_typing_indicator()
        self.update_status("Processing your request...")
        
        # Run the async task
        self.task = asyncio.run_coroutine_threadsafe(
            self.handle_user_input(user_input),
            self.loop
        )
    
    def on_enter_pressed(self, event):
        """Handle Enter key press (without Shift creates new line)"""
        if not event.state & 0x1:  # If Shift not held
            self.send_message()
            return "break"
        return None
    
    def update_status(self, message: str):
        """Update the status bar"""
        self.status_label.config(text=message)
    
    def show_settings(self):
        """Show settings dialog"""
        settings = tk.Toplevel(self.root)
        settings.title("Settings")
        settings.geometry("400x300")
        settings.resizable(False, False)
        settings.configure(bg=self.bg_color)
        
        ttk.Label(settings, text="Settings", font=('Segoe UI', 14, 'bold')).pack(pady=10)
        
        # Theme selection
        ttk.Label(settings, text="Theme:").pack(anchor='w', padx=20, pady=(10, 0))
        theme_var = tk.StringVar(value="dark")
        ttk.Radiobutton(settings, text="Dark", variable=theme_var, value="dark").pack(anchor='w', padx=40)
        ttk.Radiobutton(settings, text="Light", variable=theme_var, value="light").pack(anchor='w', padx=40)
        
        # Save button
        ttk.Button(
            settings,
            text="Save",
            command=lambda: self.change_theme(theme_var.get(), settings)
        ).pack(pady=20)
    
    def change_theme(self, theme: str, settings_window):
        """Change application theme"""
        sv_ttk.set_theme(theme)
        settings_window.destroy()
        self.update_status(f"Theme changed to {theme} mode")
    
    def open_help(self):
        """Open help documentation"""
        webbrowser.open("https://example.com/startup-mentor-help")
    
    async def handle_user_input(self, user_input):
        """Process user input and get agent response"""
        if not self.running:
            return
            
        if user_input.lower() in ["/exit", "exit"]:
            self.on_close()
            return
            
        try:
            # Get agent response
            response, new_state = await call_agent_async(
                runner, 
                "28475935", 
                self.current_backend_session.id, 
                user_input
            )
            
            self.hide_typing_indicator()
            
            # Only show the response if it's not a system message
            if response and not response.startswith(("USER_", "AGE_", "LOCATION_")):
                self.add_message("agent", response)
                
            # Update status based on missing fields
            missing_fields = get_missing_profile_fields(new_state)
            if missing_fields:
                self.update_status(f"Please provide: {', '.join(missing_fields)}")
            else:
                self.update_status("Ready to discuss your startup!")
                
        except Exception as e:
            self.hide_typing_indicator()
            self.add_message("system", f"Error: {str(e)}")
            self.update_status(f"Error: {str(e)}")
        finally:
            self.root.after(0, lambda: [
                self.input_entry.config(state=tk.NORMAL),
                self.update_send_button_state(),
                self.input_entry.focus()
            ])

# ===== Initialize services =====
db_url="sqlite:///./startup_mentor.db"
session_service = DatabaseSessionService(db_url=db_url)
initial_state = {
        "user_name":"",
        "user_age":"",
        "user_location":"",
        "user_background":"",
        "user_financial_background":"",
        "user_responsibilities":"",
        "user_goals":"",
        "user_startup_dream":"",
        "user_available_time":"",
        "user_challenges":"",
        "user_mindset":"",
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
            agent=startup_mentor_orchestrator,
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
        ui.add_message("system", "Welcome to Startup Mentor AI! How can I help you with your startup journey today?")
        
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
