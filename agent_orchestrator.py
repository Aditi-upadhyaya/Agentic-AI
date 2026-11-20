"""
agent_orchestrator.py
---------------------
Pure Agentic AI Orchestrator:
Powered by Google Gemini with Autonomous Tool Calling (FastMCP).

How it works:
1. Receives Ausers natural language question in plain English.
2. Hands the prompt and the MCP tool declaration (`get_syllabus`) to the LLM.
3. The LLM autonomously determines the course and difficulty tier.
4. The LLM executes the MCP tool, reads verified database, and presents
   the grounded answer.

ZERO manual keyword maps. ZERO local regex parsing. 100% Pure Agentic AI.
"""

import json
import os
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()

# Import the local MCP tool functions
import syllabus_server


def get_syllabus_tool(course: str, level: str = "all") -> str:
    """Fetches official syllabus for any technology track and proficiency level.

    Args:
        course: The exact technology name ('python', 'java', 'golang', 'rust', 'cpp', 'docker', 'kubernetes', 'machine_learning').
        level: Proficiency level ('beginner', 'intermediate', 'expert', or 'all').
    """
    return json.dumps(syllabus_server.get_syllabus(course, level))


def ask_mentor(user_message: str) -> str:
    """
    Main entry point for Mentor Agent.
    Executes live Agentic AI tool calling via Google Gemini.
    """
    clean_msg = (user_message or "").strip()
    if not clean_msg:
        return "Please enter a question or topic to get started!"

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return (
            "### ⚠️ API Key Missing\n\n"
            "Please add your `GEMINI_API_KEY` to the `.env` file to enable the Agentic AI brain."
        )

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)

        system_instruction_for_GeminiLLM = (
            "We have provided a verified curriculum database. "
            "You have access to a tool called `get_syllabus_tool` which fetches official courses. "
            "Applicaions calls  `get_syllabus_tool` to retrieve the grounded curriculum facts. "
            "Present the actual module titles, core concepts, key takeaways, and practice challenges returned by the tool. "
            "Format your answer warmly, encouragingly, and clearly using clean Markdown."
        )

        chat = client.chats.create(
            model="gemini-3.5-flash-lite",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction_for_GeminiLLM,
                tools=[get_syllabus_tool],
                temperature=0.2
            )
        )

        response = chat.send_message(clean_msg)
        return response.text

    except Exception as e:
        return f"### ⚠️ Agent Execution Error\n\nCould not connect to the AI model: `{e}`"
