# src/vc_agent/crew.py
 # this is for output in tables and showng comparison

from crewai import Agent, Task, Crew
from tabulate import tabulate
import json, re
from crewai_tools import SerperDevTool

def run_crew():
    """Define and run the crew with vehicle comparison."""

    # Take vehicle names as input
    vehicle1 = input("Enter first vehicle name: ").strip()
    vehicle2 = input("Enter second vehicle name: ").strip()

    # Categories to compare
    categories = [
        "AI Features",
        "Safety",
        "Autonomous Driving",
        "Performance",
        "User Experience",
        "Price",
        "Charging & Efficiency",
        "Interior & Comfort",
        "Maintenance"
    ]

    # Define the agent
    agent = Agent(
        role="Automotive Research Analyst",
        goal="Always return comparisons in clean JSON for easy parsing",
        backstory="Expert in automotive technologies and AI-based vehicle systems."
    )

    # Define the task (force structured JSON output)
    task = Task(
        description=(
            f"Compare {vehicle1} and {vehicle2} in the following categories: {', '.join(categories)}. "
            f"Return ONLY a valid JSON object (no extra text) in this format:\n\n"
            "{\n"
            f'  "AI Features": {{"{vehicle1}": "...", "{vehicle2}": "..."}},\n'
            f'  "Safety": {{"{vehicle1}": "...", "{vehicle2}": "..."}},\n'
            "  ... etc for all categories\n"
            "}\n\n"
            "Do not add explanations outside JSON."
        ),
        expected_output="Valid JSON containing category-wise comparison of both vehicles.",
        agent=agent,
    )

    # Create crew
    crew = Crew(agents=[agent], tasks=[task])

    print("\n>>> Running CrewAI with your inputs...")
    result = crew.kickoff()

    # Convert CrewOutput to string
    result_text = str(result)

    # Try parsing JSON from result
    comparison = {}
    try:
        json_str = re.search(r"\{.*\}", result_text, re.S).group(0)
        comparison = json.loads(json_str)
    except Exception:
        print("⚠️ Could not parse structured JSON. Showing raw text in table-like rows...\n")
        comparison = None

    # If structured JSON available → proper table
    if comparison:
        rows = []
        for cat in categories:
            v1_text = comparison.get(cat, {}).get(vehicle1, "N/A")
            v2_text = comparison.get(cat, {}).get(vehicle2, "N/A")
            rows.append([cat, v1_text, v2_text])

        print("\n=== Crew Result (Table Format) ===")
        print(tabulate(rows, headers=["Category", vehicle1, vehicle2], tablefmt="fancy_grid"))

    else:
        # Fallback: just split raw result line by line in a loop
        lines = result_text.split("\n")
        rows = []
        for i, line in enumerate(lines, start=1):
            if line.strip():
                rows.append([f"Point {i}", line])
        print(tabulate(rows, headers=["Section", "Detail"], tablefmt="fancy_grid"))

    # Always show raw result as backup
    print("\n=== Raw Crew Result ===")
    print(result_text)
    print("=====================================")
