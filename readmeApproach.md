# Agentic AI & MCP Learning Project: Python Mentor Agent

**Student:** Aditi  
**Instructor:** Dad  
**Focus:** Agentic AI, Model Context Protocol (MCP), Tool Calling, and Hybrid Reasoning with Python  

---

## 1. Executive Summary & Vision

This document outlines the finalized pedagogical approach for teaching **Agentic AI** and **Model Context Protocol (MCP)** using Python.

Instead of heavy corporate topics (such as incident management systems or enterprise cloud infra), this project is built around something directly relevant and exciting for her: **An Interactive Python Learning & Quiz Mentor Agent**.

The project directly demonstrates the **hybrid architecture** of modern production AI:
1. **The MCP Half (External Grounded Fact):** Fetching the official syllabus from Dad's private database.
2. **The Pure LLM Half (Internal Brain & Creativity):** Generating fun, interactive quiz questions directly from the model's native intelligence.

---

## 2. The 2-Stage Learning Progression

To make the value of Agentic AI and MCP crystal clear, the project is taught in two distinct stages:

```
┌────────────────────────────────────────────────────────────────────────┐
│  STAGE 1: Traditional Chatbot (Without MCP & Without Agency)           │
│                                                                        │
│  Aditi asks: "Give me the syllabus for Python for beginners."          │
│               │                                                        │
│               ▼                                                        │
│  [Prompt] ──> [LLM Brain] ──> [Generic Internet Syllabus]              │
│                                                                        │
│  Key Lesson: The AI guesses from public training data.                 │
│              It cannot see Dad's private, verified syllabus.           │
└────────────────────────────────────────────────────────────────────────┘

                                   │
                                   ▼

┌────────────────────────────────────────────────────────────────────────┐
│  STAGE 2: The Agentic Mentor (With MCP & Thinking Chain)               │
│                                                                        │
│  Aditi asks: "Give me the Python syllabus and quiz me on Topic 1!"     │
│               │                                                        │
│               ▼                                                        │
│  [Thought 1]: "I need Dad's syllabus. Let me call the MCP tool."      │
│               │                                                        │
│               ▼                                                        │
│  [Action 1] : Calls `get_syllabus(topic='python')` via MCP             │
│               │                                                        │
│               ▼                                                        │
│  [Observation 1]: Receives private DB: Topic 1 = "Variables & Boxes"  │
│               │                                                        │
│               ▼                                                        │
│  [Thought 2]: "Topic 1 is Variables. Now I will create a fun quiz     │
│                using my own brain without calling any tools."          │
│               │                                                        │
│               ▼                                                        │
│  [Final Output]: Displays approved syllabus + 3 interactive quiz Qs!   │
│                                                                        │
│  Key Lesson: The AI acts autonomously, blends private data (MCP) with  │
│              native creativity (LLM), and solves multi-step goals.     │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. The 7 Core AI Concepts Aditi Will Master

| # | Concept | What It Teaches Her |
| :-: | :--- | :--- |
| **1** | **Multi-Step Task Planning** | The AI breaks a complex request into sequential sub-tasks: *First get syllabus $\rightarrow$ Then inspect topic $\rightarrow$ Then build quiz.* |
| **2** | **Parametric vs. Non-Parametric Memory** | Understanding the two types of AI knowledge: <br>• **Non-Parametric**: Grounded facts fetched live from external databases.<br>• **Parametric**: Creative reasoning from model weights. |
| **3** | **Autonomous Tool Calling (Agency)** | Teaching the AI to decide **when** to call an external tool (syllabus) and **when** to answer from its own brain (quiz). |
| **4** | **Grounding & Zero Hallucination** | How private tools prevent the AI from making up inaccurate information. |
| **5** | **The ReAct Loop** | Watching the standard industry agent loop live in terminal: **Reason $\rightarrow$ Act $\rightarrow$ Observe $\rightarrow$ Answer**. |
| **6** | **Universal Protocol Engineering (MCP)** | Why MCP acts as the *"universal USB cable"* connecting AI models to private tools and databases. |
| **7** | **Tone & Persona Adaptation** | Transforming cold JSON database rows into encouraging, age-appropriate learning analogies. |

---

## 4. Technical Architecture & Tech Stack

- **Language:** Python 3.10+
- **MCP Framework:** `FastMCP` (Official Python MCP SDK) — simple decorator-based tool creation (`@mcp.tool()`).
- **LLM Client:** Anthropic Claude / OpenAI / Google Gemini API via Python SDK.
- **Database:** SQLite or lightweight local JSON file (`syllabuses.json`) to keep it simple, visual, and editable.
- **Interface:** Interactive Python CLI with colored terminal output showing the agent's internal "Thoughts".

### Architecture Diagram:
```
+-------------------------------------------------------------------+
|                        ADITI'S TERMINAL                           |
+-------------------------------------------------------------------+
                                  │
                                  ▼
+-------------------------------------------------------------------+
|                  AGENTIC ORCHESTRATOR (Python)                    |
|                                                                   |
|   1. Receives Aditi's natural language request                    |
|   2. Passes system prompt + available tool declarations to LLM    |
|   3. Executes MCP tool calls if requested by LLM                  |
|   4. Returns tool observations back into context                  |
|   5. Prints internal "Thinking Chain" for transparency            |
+-------------------------------------------------------------------+
           │                                      │
           │ (MCP Protocol / JSON-RPC)            │ (API Prompt & Generation)
           ▼                                      ▼
+-----------------------+              +-----------------------+
|   LOCAL MCP SERVER    |              |       LLM BRAIN       |
|  (`syllabus_server`)  |              |   (Claude / GPT-4o)   |
|                       |              |                       |
| Exposes Tool:         |              | • Intent parsing      |
| `get_syllabus()`      |              | • Creative quiz gen   |
+-----------------------+              | • Pedagogical tone    |
           │                           +-----------------------+
           ▼
+-----------------------+
|    LOCAL DATABASE     |
| (Dad's Python Tracks) |
+-----------------------+
```

---

## 5. 4-Week Step-by-Step Curriculum for Aditi

### Week 1: "The Chatbot in a Box" (Baseline Understanding)
- **Goal:** Set up a simple Python script connecting to an LLM.
- **Experiment:** Ask for a Python syllabus.
- **Observation:** Notice that the syllabus is generic and comes from the open internet. Discuss why the model cannot see Dad's specific company/personal curriculum.

### Week 2: "Building the Magic Cable" (First FastMCP Server)
- **Goal:** Create a 15-line MCP Server in Python using `FastMCP`.
- **Hands-on:** Build a small SQLite or JSON database containing Dad's official beginner Python syllabus:
  - *Module 1:* Magic Boxes (Variables & Data Types)
  - *Module 2:* Traffic Lights (Conditionals & If/Else)
  - *Module 3:* Rollercoasters (Loops & Repetition)
- Expose the function `@mcp.tool() def get_syllabus(topic: str)`.

### Week 3: "Connecting Brain to Cable" (MCP Tool Calling)
- **Goal:** Connect the LLM Client to the local MCP Server.
- **Experiment:** Ask the exact same prompt from Week 1.
- **The "Aha!" Moment:** Watch the AI call `get_syllabus` and present Dad's exact curriculum instead of a random internet version.

### Week 4: "The Thinking Chain & Quiz Master" (Full Agentic Loop)
- **Goal:** Upgrade the prompt to a multi-step challenge: *"Give me the syllabus and quiz me on Module 1!"*
- **Hands-on:** Add code to print the agent's internal thoughts to terminal:
  - `[Thinking]: I need the syllabus first... calling get_syllabus()`
  - `[Observation]: Module 1 is Variables.`
  - `[Thinking]: Now creating a 3-question quiz using my own brain...`
- Aditi interacts with her completed, autonomous Python tutor agent!

---

## 6. Dad's Coaching Tips for Aditi

1. **Use Real-World Analogies:**
   - **Agent vs Chatbot:** Chatbot is a genius stuck in a room who can only talk. An Agent is that genius with hands and a utility belt.
   - **MCP:** The universal USB-C cable for AI.
2. **Docstrings are Prompts for Code:**
   - Teach her that the docstring inside a Python function (`"""Fetches the official syllabus..."""`) is what the AI reads to decide which tool to pick.
3. **Always Print the Thoughts:**
   - Always display `Thought: ...` in the terminal. Seeing the AI "talk to itself" before acting is where the deepest learning happens.
4. **Celebrate When the Agent Makes a Mistake:**
   - If the agent calls the wrong tool, debug it like a mystery game: *"Why did the robot choose that? How can we make the tool description clearer?"*

---

*Authored for the learning journey of Aditi — October 2026*
