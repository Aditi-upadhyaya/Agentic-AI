"""
app.py
------
Stage 1 Flask Web Application:
Presents a simple, clean interface for users to type natural language questions
and see Dad's verified syllabus formatted cleanly and beautifully.
"""

import os
from flask import Flask, render_template, request, jsonify
import syllabus_server
import agent_orchestrator

app = Flask(__name__)


@app.route("/")
def home():
    """Serves the clean Stage 1 text-box interface."""
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """
    Receives users natural language question, queries the MCP-backed
    agent orchestrator, and returns the formatted response.
    """
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({
            "status": "error",
            "response": "Please enter a question or course name to get started!"
        })

    # Call the Stage 1 agent orchestrator
    response_text = agent_orchestrator.ask_mentor(user_message)

    return jsonify({
        "status": "success",
        "response": response_text
    })


@app.route("/api/courses", methods=["GET"])
def courses():
    """Returns the list of available courses from Dad's database."""
    return jsonify(syllabus_server.list_available_courses())


if __name__ == "__main__":
    print("\n=======================================================")
    print(" 🎓 Tech Mentor — Stage 1 is Running!")
    print(" Open your browser and go to: http://127.0.0.1:5000")
    print("=======================================================\n")
    app.run(host="127.0.0.1", port=5000, debug=True)
