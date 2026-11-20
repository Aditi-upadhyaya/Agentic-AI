"""
syllabus_server.py
------------------
Local FastMCP server exposing  private curriculum database.
Supports 7 technologies (Python, Java, C++, Rust, Docker, Kubernetes, Machine Learning)
across 3 proficiency tiers (beginner, intermediate, expert).
"""

import json
import os
from typing import Any, Dict, List

# Path to private syllabus database
DB_PATH = os.path.join(os.path.dirname(__file__), "syllabus.json")


def load_database() -> Dict[str, Any]:
    """Loads the syllabus database from disk."""
    if not os.path.exists(DB_PATH):
        return {}
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_syllabus(course: str, level: str = "all") -> Dict[str, Any]:
    """
    Fetches  official syllabus for any technology track and proficiency level.

    Args:
        course: The exact technology name. Must be one of:
                'python', 'java', 'golang', 'rust', 'cpp',
                'docker', 'kubernetes', 'machine_learning'.
        level: Proficiency level: 'beginner', 'intermediate', 'expert', or 'all'
               (defaults to 'all' if user asks generally).
    """
    db = load_database()
    
    # Normalize input
    course_clean = (course or "").strip().lower().replace(" ", "_")
    level_clean = (level or "all").strip().lower()

    # Direct database lookup - zero manual alias maps needed!
    if course_clean not in db:
        return {
            "status": "not_found",
            "message": f"Course '{course}' not found in  curriculum database.",
            "available_courses": list(db.keys())
        }

    course_data = db[course_clean]

    # Return all levels if requested
    if level_clean in ("all", "overview", "general", ""):
        return {
            "status": "success",
            "course_slug": course_clean,
            "course_name": course_data["course_name"],
            "category": course_data["category"],
            "overview": course_data["overview"],
            "levels_overview": {
                lvl: {
                    "tier_summary": data["tier_summary"],
                    "modules_count": len(data["modules"]),
                    "module_titles": [m["title"] for m in data["modules"]]
                }
                for lvl, data in course_data["levels"].items()
            }
        }

    # Return specific tier
    if level_clean in course_data["levels"]:
        return {
            "status": "success",
            "course_slug": course_clean,
            "course_name": course_data["course_name"],
            "category": course_data["category"],
            "level": level_clean,
            "tier_details": course_data["levels"][level_clean]
        }

    return {
        "status": "invalid_level",
        "message": f"Level '{level}' not recognized for {course_data['course_name']}.",
        "available_levels": ["beginner", "intermediate", "expert", "all"]
    }


def list_available_courses() -> List[Dict[str, str]]:
    """
    Returns a directory of all available courses, categories, and supported levels in  database.
    """
    db = load_database()
    directory = []
    for slug, data in db.items():
        directory.append({
            "slug": slug,
            "name": data.get("course_name", slug),
            "category": data.get("category", "General"),
            "levels": list(data.get("levels", {}).keys())
        })
    return directory


# If FastMCP is installed, register as an official MCP server
try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("SyllabusServer")

    @mcp.tool()
    def get_syllabus_tool(course: str, level: str = "all") -> str:
        """Fetches  official syllabus for any technology track and proficiency level."""
        return json.dumps(get_syllabus(course, level), indent=2)

    @mcp.tool()
    def list_available_courses_tool() -> str:
        """Returns a directory of all available courses and supported levels in  database."""
        return json.dumps(list_available_courses(), indent=2)

except ImportError:
    mcp = None


if __name__ == "__main__":
    # Quick self-test verification
    print("Testing get_syllabus('python', 'beginner'):")
    res = get_syllabus("python", "beginner")
    print(f"Status: {res.get('status')}, Modules count: {len(res.get('tier_details', {}).get('modules', []))}")
    print("\nAvailable courses in  database:")
    for c in list_available_courses():
        print(f" - {c['name']} ({c['slug']}) [{c['category']}]")
