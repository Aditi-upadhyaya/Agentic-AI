# Autonomous Agentic AI Curriculum Mentor

> **An AI-powered technical mentor that understands natural-language learning queries, autonomously identifies the required curriculum, retrieves verified information through Model Context Protocol (MCP) tools, and delivers grounded learning guidance.**

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20Backend-black?logo=flask)](https://flask.palletsprojects.com/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-LLM-4285F4?logo=google)](https://ai.google.dev/)
[![MCP](https://img.shields.io/badge/Model%20Context%20Protocol-FastMCP-purple)](https://modelcontextprotocol.io/)

---

## 📌 Overview

**Autonomous Agentic AI Curriculum Mentor** is a full-stack AI mentoring platform built to demonstrate how modern **Agentic AI**, **LLM tool calling**, and the **Model Context Protocol (MCP)** can be combined to create grounded, enterprise-oriented AI applications.

Instead of relying on hard-coded keyword matching, regular expressions, or manually maintained intent mappings, the system allows **Google Gemini** to interpret a user's natural-language question and autonomously determine which curriculum information it needs.

The agent can identify:

- The requested technology/course
- The learner's proficiency level
- The appropriate MCP tool to call

It then retrieves the relevant information from a structured curriculum knowledge base and uses the verified data to generate the final response.

### Example

A user can simply ask:

> **"What should I learn in Rust as a beginner?"**

The system can infer:

```text
course = rust
level  = beginner
```

and retrieve the corresponding curriculum through the MCP tool before generating the response.

---

## ✨ Key Features

### 🧠 Autonomous Natural-Language Understanding

Users do not need to provide structured parameters.

Instead of:

```text
course=rust&level=beginner
```

they can simply ask:

```text
What do we learn in Rust beginner?
```

Google Gemini interprets the request and determines the appropriate tool arguments automatically.

---

### 🔧 Automatic Function Calling

The project uses Google's GenAI SDK with **Automatic Function Calling (AFC)**.

The `get_syllabus_tool()` function is exposed to Gemini as an available tool. Gemini decides when the tool is required and supplies the appropriate arguments.

Conceptually:

```text
User Query
    ↓
Google Gemini
    ↓
Determines course + proficiency level
    ↓
get_syllabus_tool(course, level)
    ↓
Curriculum Database
    ↓
Verified JSON data
    ↓
Gemini
    ↓
Grounded mentor response
```

This eliminates the need for manually parsing user queries using brittle regex rules or large keyword/alias maps.

---

### 🔌 Model Context Protocol (MCP)

The project demonstrates the use of **FastMCP** to expose curriculum data as callable tools.

The MCP server provides functions for:

- Retrieving syllabus information
- Listing available courses
- Accessing curriculum by proficiency level

The tool layer acts as a controlled interface between the AI model and the underlying knowledge repository.

---

### 🎯 Grounded Responses

The mentor does not need to invent curriculum content.

Instead, curriculum information is retrieved directly from the project's structured `syllabus.json` knowledge repository.

The system supports three proficiency levels:

- 🟢 Beginner
- 🟡 Intermediate
- 🔴 Expert

This architecture helps keep curriculum-specific responses grounded in the available source data.

---

### 🚫 No Manual Intent Mapping

Traditional implementations might contain logic such as:

```python
if "python" in query:
    course = "python"
elif "rust" in query:
    course = "rust"
```

This project intentionally avoids that approach.

Gemini's semantic understanding determines the intent and extracts the relevant parameters before invoking the tool.

---

### 🌐 Full-Stack Web Interface

The project includes a Flask-based web application that provides:

- Natural-language chat interface
- Course discovery endpoint
- AI-generated curriculum responses
- Markdown-formatted mentor responses
- Interactive frontend experience

The main API flow is:

```text
Browser
   ↓
POST /chat
   ↓
Flask
   ↓
Agent Orchestrator
   ↓
Gemini + Tool Calling
   ↓
MCP Curriculum Server
   ↓
syllabus.json
   ↓
Grounded Response
   ↓
Browser
```

---

## 🏗️ System Architecture

```text
                    ┌──────────────────────────┐
                    │        USER / BROWSER    │
                    │                          │
                    │ "What should I learn    │
                    │  in Rust as a beginner?" │
                    └────────────┬─────────────┘
                                 │
                                 │ HTTP POST /chat
                                 ▼
                    ┌──────────────────────────┐
                    │       FLASK SERVER       │
                    │         app.py           │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │   AGENT ORCHESTRATOR     │
                    │  agent_orchestrator.py   │
                    └────────────┬─────────────┘
                                 │
                                 │ Prompt + Tool
                                 ▼
                    ┌──────────────────────────┐
                    │     GOOGLE GEMINI        │
                    │                          │
                    │ Semantic Understanding   │
                    │ + Automatic Tool Calling │
                    └────────────┬─────────────┘
                                 │
                                 │ Tool Call
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │      FASTMCP SERVER      │
                    │   syllabus_server.py     │
                    └────────────┬─────────────┘
                                 │
                                 │ Direct Lookup
                                 ▼
                    ┌──────────────────────────┐
                    │     SYLLABUS DATABASE    │
                    │       syllabus.json      │
                    └────────────┬─────────────┘
                                 │
                                 │ Verified Data
                                 ▼
                    ┌──────────────────────────┐
                    │     GOOGLE GEMINI        │
                    │                          │
                    │ Grounded Response        │
                    │ + Markdown Formatting    │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │      FLASK RESPONSE      │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │        USER UI           │
                    │   Curriculum Guidance    │
                    └──────────────────────────┘
```

The repository also contains a more detailed execution-flow reference documenting this request → Gemini → tool → database → Gemini → browser lifecycle. 

---

## 🔄 Agent Execution Flow

The complete request lifecycle is:

### 1. User submits a question

Example:

```text
What should I learn in Rust as a beginner?
```

### 2. Flask receives the request

The frontend sends the user's message to:

```text
POST /chat
```

The Flask application passes the message to the agent orchestrator.

### 3. Gemini receives the query and available tool

The orchestrator creates a Gemini client and exposes:

```text
get_syllabus_tool(course, level)
```

to the model.

### 4. Gemini determines the required parameters

Gemini semantically interprets the question:

```text
course → rust
level  → beginner
```

No manual regex or keyword mapping is required.

### 5. Gemini invokes the tool

The tool receives:

```python
get_syllabus_tool("rust", "beginner")
```

### 6. MCP accesses the curriculum repository

The tool calls the local syllabus server, which performs a direct lookup against:

```text
syllabus.json
```

### 7. Verified curriculum data is returned

The relevant modules, concepts, summaries, and practice information are returned to the agent.

### 8. Gemini synthesizes the final response

Gemini uses the retrieved curriculum information to produce a clear, encouraging Markdown response.

### 9. Flask returns the response

The final response is sent back to the browser and rendered in the frontend.

---

## 🧩 Technology Stack

| Technology | Purpose |
|---|---|
| **Python** | Core application and agent logic |
| **Google Gemini** | Natural-language understanding and tool calling |
| **Google GenAI SDK** | Gemini API integration |
| **FastMCP** | MCP tool/server layer |
| **Flask** | Web backend and REST API |
| **HTML / CSS / JavaScript** | Interactive frontend |
| **JSON** | Curriculum knowledge repository |
| **python-dotenv** | Environment variable management |

---

## 📚 Curriculum Knowledge Base

The project includes a modular curriculum repository in:

```text
syllabus.json
```

The current knowledge base covers **8 technology tracks**:

- Python
- Java
- Golang
- Rust
- C++
- Docker
- Kubernetes
- Machine Learning

Each technology contains curriculum information organized into:

```text
Beginner
Intermediate
Expert
```

The syllabus server performs direct database lookups and returns structured information based on the requested course and proficiency level.

---

## 📁 Project Structure

```text
Agentic-AI/
│
├── app.py
│   └── Flask web application and API routes
│
├── agent_orchestrator.py
│   └── Gemini-powered agent and automatic tool calling
│
├── syllabus_server.py
│   └── Curriculum retrieval layer and FastMCP server
│
├── syllabus.json
│   └── Structured curriculum knowledge base
│
├── templates/
│   └── Frontend HTML templates
│
├── static/
│   └── CSS, JavaScript and frontend assets
│
├── promo_video/
│   └── Project demonstration assets
│
├── .env.example
│   └── Environment variable template
│
├── .gitignore
│   └── Files excluded from version control
│
├── run.bat
│   └── Windows helper script for running the application
│
├── flow.md
│   └── Detailed agent execution flow
│
├── explaination.md
│   └── Project explanation and implementation notes
│
├── codeexplaination.md
│   └── Code-level explanations
│
├── databaseDesing.md
│   └── Knowledge-base/database design notes
│
├── LearningImp.md
│   └── Learning and implementation insights
│
├── steps.md
│   └── Project development/setup steps
│
└── understanding.md
    └── Conceptual understanding and learning notes
```

---

## 🚀 Getting Started

### Prerequisites

Make sure you have:

- Python 3.x
- A Google Gemini API key
- Git

---

### 1. Clone the repository

```bash
git clone https://github.com/Aditi-upadhyaya/Agentic-AI.git
cd Agentic-AI
```

---

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

---

### 3. Install dependencies

Install the required Python packages used by the project:

```bash
pip install flask python-dotenv google-genai mcp
```

---

### 4. Configure the Gemini API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

**Never commit your `.env` file or API key to GitHub.**

The repository includes `.env.example` as a safe configuration template.

---

### 5. Run the application

```bash
python app.py
```

Or, on Windows, use:

```bash
run.bat
```

The Flask application will start locally and provide the web interface.

---

## 🔌 API Endpoints

### `GET /`

Loads the main web interface.

---

### `POST /chat`

Accepts a natural-language user query.

Example request:

```json
{
  "message": "What should I learn in Python as an intermediate developer?"
}
```

Example response:

```json
{
  "status": "success",
  "response": "..."
}
```

---

### `GET /api/courses`

Returns the list of available curriculum tracks and their supported levels.

---

## 🧠 Why This Architecture?

A conventional chatbot might work like this:

```text
User
 ↓
LLM
 ↓
Generated Answer
```

The problem is that the model may not have access to the latest or authoritative information required by the application.

This project instead introduces a controlled tool layer:

```text
User
 ↓
LLM
 ↓
Tool Decision
 ↓
MCP Tool
 ↓
Verified Knowledge
 ↓
LLM
 ↓
Grounded Answer
```

This architecture separates:

**Reasoning / intent understanding**

from

**Knowledge retrieval**

making the system easier to control, extend, and integrate with enterprise data sources.

---

## 🛡️ Grounding Strategy

The curriculum-specific information is stored separately from the language model in the structured knowledge repository.

The agent is instructed to use the provided curriculum tool to retrieve:

- Module titles
- Core concepts
- Key takeaways
- Practice challenges
- Proficiency-specific curriculum information

The retrieved data is then supplied to Gemini for response synthesis.

This provides a practical pattern for building AI applications where responses should be grounded in an organization's trusted internal knowledge rather than relying exclusively on the model's pretrained knowledge.

---

## 💡 Key Engineering Concepts Demonstrated

This project demonstrates several important concepts in modern AI application development:

### Agentic AI

The LLM is given access to tools and determines when those tools are required to answer a user's request.

### Automatic Function Calling

Gemini can translate natural-language intent into structured function arguments and invoke the appropriate Python function.

### Model Context Protocol

FastMCP provides a standardized tool interface between the AI model and application data.

### Semantic Intent Detection

Natural-language understanding replaces brittle keyword matching and manually maintained aliases.

### Grounded Generation

The final response is based on retrieved curriculum data rather than requiring the model to independently generate curriculum facts.

### Full-Stack AI Integration

The project connects:

```text
Frontend
   ↓
Flask API
   ↓
Agent
   ↓
LLM
   ↓
MCP Tools
   ↓
Knowledge Base
```

into a single working application.

---

## 🎯 Enterprise Use Case

Although this project uses a curriculum knowledge base, the architecture is designed to demonstrate a broader enterprise pattern.

The same architecture can be adapted to internal systems such as:

- Employee training platforms
- Internal documentation assistants
- HR knowledge systems
- Product support assistants
- Corporate learning platforms
- Internal policy assistants
- Technical onboarding systems
- Enterprise knowledge retrieval

For example:

```text
Employee Question
       ↓
Enterprise AI Agent
       ↓
MCP Tool
       ↓
Internal Database / API
       ↓
Verified Enterprise Data
       ↓
Grounded AI Response
```

This makes MCP-based tool integration a practical approach for connecting LLMs with controlled enterprise data sources.

---

## 📈 Future Improvements

Potential future extensions include:

- Persistent conversation memory
- User authentication and personalized learning paths
- Progress tracking
- Quiz and assessment generation
- Additional enterprise data sources
- Database-backed curriculum management
- Streaming responses
- More MCP tools
- Multi-agent curriculum planning
- Learning analytics
- Deployment using Docker and cloud infrastructure
- Automated evaluation of response grounding
- Role-based enterprise access control

---

## ⚠️ Security

This project uses a Gemini API key through an environment variable.

Make sure that:

```text
.env
```

is included in `.gitignore`.

Never hard-code API keys inside Python source files or commit them to a public repository.

If an API key is accidentally exposed, revoke it immediately and generate a new one.

---

## 📖 Documentation

Additional implementation and learning documentation is available in the repository:

- `flow.md` — Complete agent execution flow
- `explaination.md` — Project explanation
- `codeexplaination.md` — Code-level explanation
- `databaseDesing.md` — Curriculum data design
- `steps.md` — Development/setup steps
- `LearningImp.md` — Learning insights
- `understanding.md` — Conceptual understanding

---

## 👩‍💻 Author

**Aditi Upadhyaya**

Built as a practical exploration of **Agentic AI, Google Gemini, Automatic Function Calling, FastMCP, and grounded enterprise AI architectures.**

---

## ⭐ Project Highlights

```text
Natural Language Understanding
          +
Automatic Function Calling
          +
Model Context Protocol
          +
Verified Knowledge Retrieval
          +
Grounded Generation
          +
Flask Full-Stack Application
          =
Autonomous AI Curriculum Mentor
```

---

### 📌 Project Goal

The goal of this project is not simply to build another chatbot.

It is to demonstrate how an LLM can move beyond generating text and instead **understand intent, select tools, retrieve trusted information, and synthesize that information into a useful response** — forming the foundation of practical Agentic AI systems.
