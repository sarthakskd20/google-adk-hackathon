## 🚀 Installation Instructions

Follow these steps to set up and run the project locally:

### 📦 Step 1: Download the Repository

* Click on the green `Code` button at the top of the repository page.
* Select **Download ZIP** and extract it to your desired location.

### 📂 Step 2: Navigate to the Project Directory

```bash
cd path/to/extracted/folder
```

### 🐍 Step 3: Create a Virtual Environment

```bash
python -m venv .venv
```

> This will create a `.venv` folder containing your isolated Python environment.

### ⚡ Step 4: Activate the Virtual Environment

* **For Windows CMD**:

  ```bash
  .venv\Scripts\activate.bat
  ```
* **For Windows PowerShell**:

  ```powershell
  .venv\Scripts\Activate.ps1
  ```

### 📥 Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### 🔐 Step 6: Set Up Environment Variables

* Create a `.env` file in the root folder.
* Copy contents from `.env.example` into `.env`.
* Make sure to insert your own **API key(s)** where required.

### ▶️ Step 7: Run the Application

```bash
python main.py
```

Once this is done, your agent will start and launch with the proper user interface. You're ready to go! 🎉


### Explanation:

This system, called the **Startup Mentor Orchestrator**, is designed to help you build your startup. Think of it like a smart assistant that guides you step-by-step. Here's how it works, explained like a **flowchart** (a diagram showing steps and decisions):

---

### **1. Starting Your Session**
* **Start (A)**: This is where everything begins! When you first interact with the system, it's like pressing a "start" button.
* **New Session? (B)**: The system first checks if you've talked to it before.
    * If **Yes** (it's your first time): It shows you a friendly **Welcome Message (C)**, something like "👋 Hi there! Let's build your startup!" To make sure it doesn't show you this message again, it secretly marks down that it `_has_displayed_welcome=True` **(D)**.
    * If **No** (you've talked to it before): It skips the welcome message and goes straight to the next step.
* **Invoke `user_understanding_agent` (E)**: This is like a smart helper that starts gathering your information, like your background, your startup idea, and your skills. It also makes sure the information you give is valid.

---

### **2. Making Sure Your Profile is Complete (The "Profile Validation Loop")**
* **Is User Profile Complete? (F)**: The system checks if it has all the necessary information about you and your startup idea.
    * If **No** (something's missing): It enters a special loop to get all the details.
        1.  **Collect Missing Fields (G)**: It asks you for any information it needs, for example, "What’s your budget?"
        2.  **Profile Valid? (H)**: After you provide the information, the system checks if it makes sense. For instance, if you type "banana" for your budget, it knows that's not right.
            * If it's **Invalid**: It goes back to **G** and asks you to try again. It will keep doing this until you give it valid information.
            * If it's **Valid**: Great! It moves on to confirm that your profile is complete **(K)**.
    * If **Yes** (your profile is already complete): It skips all the asking and goes straight to confirming your profile completion **(K)**.

> **Important Point**: This system is really persistent! It **won't move on** until it has all the necessary and correct information from you.

---

### **3. Getting Ready for Mentorship**
* **Confirm Profile Completion (K)**: Once your profile is all set, the system tells you, "✅ Profile complete! Let’s begin mentoring."
* **Activate `startup_llm_mentor_agent` (L)**: This is like the main brain of the system, powered by a very smart AI called **Gemini 2.5 Pro LLM**. It now takes over to guide you, using various tools to help.

---

### **4. Answering Your Questions (Query Handling & Sub-Agent Orchestration)**
* **User Query Received (M)**: You ask a question, like "How do I patent my idea?"
* **Gemini 2.5 Pro Analyzes Intent (N)**: The main brain (Gemini) figures out what kind of question you're asking – is it about legal stuff, money, or market research?
* **Route to Specialized Sub-Agent (O)**: Based on your question, Gemini sends it to the right expert helper (we call these **sub-agents**).
    * **Sub-Agents (P-S)**: These are like mini-experts for different topics:
        * `startup_execution_roadmap_planner_agent`: Helps with business plans.
        * `market_insight_strategist_agent`: Helps analyze competitors or markets.
        * `legal_foundation_guide_agent`: Gives advice on things like patents and copyrights.
        * (There are other experts not listed here too!)
* **Synthesize Response (T)**: The main brain (Gemini) takes the answers from the expert helpers and puts them together into one clear, complete answer for you.
* **Return Output to User (U)**: Finally, it sends you the answer, for example, "To patent your idea: 1. File a provisional..."

---

### **5. Staying Connected (Continuous Interaction)**
* **Loop Back to (M)**: After giving you an answer, the system goes back to **(M)** and waits for your next question. This means it's always ready to help you, in an **endless loop**, as long as your session is active.

---

### **Why This System is So Smart**
* **Remembers Things**: It keeps track of your profile data and whether it has shown you the welcome message.
* **Corrects Itself**: If you enter wrong information, it will politely ask you to fix it until it's right.
* **Picks the Right Tool**: The main brain (Gemini) is smart enough to know which expert helper (sub-agent) is best for your question. It doesn't just follow a fixed set of rules.
* **Easy to Grow**: New expert helpers can be added or removed easily without messing up the whole system.

---

### **Let's See an Example**
Imagine you:
1.  **First time using the system**: You get the welcome message and start giving some details about your startup.
2.  **Missing info**: The system realizes you didn't provide your budget. It asks, and you keep trying until you enter a valid number.
3.  **Ask a question**: You then ask, "How do I enter the German market?"
    * **Routing**: The main brain (Gemini) sends this to the `market_insight_strategist_agent` (the market expert).
    * **Output**: The system responds with helpful advice like, "Germany requires EU compliance certificates. Steps: 1. Get CE marking..."

---

The **DreamWeaver AI Startup Mentor** is designed to be your ultimate virtual guide and partner in the entrepreneurial journey. Based on the detailed explanation of its mechanism, here are its special features:

### **Core AI Powerhouse:**
1.  **Gemini 2.5 Pro LLM as the Central Brain:** At its heart, DreamWeaver uses a highly advanced AI, Gemini 2.5 Pro LLM. This means it can understand complex questions, generate human-like responses, and reason across various business domains, acting as the primary intelligent interface.
2.  **Intent-Driven Routing (Smart Delegation):** When you ask a question, the system doesn't just give a generic answer. It cleverly **analyzes the "intent"** of your query (e.g., "Is this about legal matters, marketing, or finances?"). This allows it to then send your question to the most appropriate specialized expert within its system.
3.  **Modular Sub-Agent Architecture (Specialized Experts):** DreamWeaver isn't a single "know-it-all" AI. It's built with various "sub-agents," each acting as a mini-expert in a specific area. This includes:
    * `startup_execution_roadmap_planner_agent` (for business planning and strategy)
    * `market_insight_strategist_agent` (for understanding your market and competitors)
    * `legal_foundation_guide_agent` (for legal advice, intellectual property, etc.)
    * *(And other unlisted specialized agents, allowing for comprehensive support)*
    This modularity means it can provide deep, focused advice on specific topics.

### **User-Centric & Adaptive Experience:**
4.  **Intelligent Session Initialization:** It gracefully welcomes new users with personalized messages and seamlessly integrates returning users into their ongoing journey, ensuring a smooth start every time.
5.  **Robust Profile Validation Loop (No Data Gaps):** This is a key differentiator. DreamWeaver ensures it has all the necessary information about you and your startup. If something's missing or incorrect, it will **persistently and politely prompt you** until valid data is provided. This prevents incomplete profiles from hindering effective mentorship.
6.  **Personalized Learning & Guidance:** By collecting detailed user profiles, DreamWeaver can tailor its advice and resources to your unique background, startup idea, and specific challenges, rather than offering generic information.
7.  **Continuous Interaction (Always Available):** Unlike human mentors who have limited availability, DreamWeaver is designed to be an "infinite loop" that's always ready for your next question or challenge. It operates 24/7, providing on-demand advice.

### **Operational Excellence & Scalability:**
8.  **State Persistence:** The system "remembers" your progress, profile details, and previous interactions (`ctx.session.state`). This means you can pick up exactly where you left off, and the system maintains context throughout your entrepreneurial journey.
9.  **Asynchronous Validation (Real-time Feedback):** The profile validation is non-blocking, meaning you get real-time feedback on your inputs. If you make a mistake, it immediately guides you to correct it without interrupting the flow of your interaction.
10. **Dynamic Tool Selection (No Hardcoded Rules):** The AI intelligently decides which sub-agent (tool) to use based on your query's intent. This isn't based on rigid rules but on its advanced understanding, making it flexible and adaptable to new types of questions.
11. **Scalable and "Plug-and-Play" Architecture:** The modular design means new sub-agents (new expert helpers for new domains ) can be easily added or removed without disrupting the core system. This makes DreamWeaver highly scalable and future-proof.
12. **Self-Healing and Error Reduction:** The automatic retry mechanism for invalid data inputs helps correct common user errors on the spot, reducing the need for human intervention or support.

In essence, the **DreamWeaver AI Startup Mentor** combines powerful AI intelligence with a highly structured, user-friendly, and continuously available platform to provide comprehensive, personalized, and proactive guidance to aspiring and existing startup founders.
Do you have any specific part of this process you'd like me to explain in more detail?

### Flowchart Mechanism
```
graph TD
  A[Startup Mentor: Greet User] --> B[SubAgent_ProfileCollector]
  B --> C{Profile Complete?}
  C -->|No| D[Loop: Request Missing/Clarify Irrelevant Data]
  D --> B
  C -->|Yes| E{Has Startup Plan?}
  E -->|Yes| F[SubAgent_PlanValidator]
  F --> G[SubAgent_SWOTAnalyzer]
  G --> H[SubAgent_LegalAdvisor]
  H --> I{Legal?}
  I -->|No| J[Reject Plan + Explain]
  I -->|Yes| K[Suggest Improvements]
  K --> L[Revised Plan]
  E -->|No| M[SubAgent_IdeaGenerator]
  M --> N[Propose 3 Ideas]
  N --> O[User Selects 1]
  O --> G
  L & O --> P[SubAgent_ImplementationStrategist]
  P --> Q[Phase 1: Pre-Launch]
  Q --> R[Phase 2: Launch]
  R --> S[Phase 3: Growth]
  S --> T[SubAgent_SupportBot: Follow-ups]
  T -->|User Queries| P
```
