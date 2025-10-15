# src/vc_agent/main.py
from vc_agent.crew import VehicleAICrew

def run_cli():
    crew_instance = VehicleAICrew().crew()

    while True:
        query = input("\nAsk me about vehicles (or type 'exit'): ")
        if query.lower() in ["exit", "quit"]:
            break

        result = crew_instance.kickoff(inputs={"query": query})
        print("\n=== Agent Response ===\n")
        print(result)
        print("\n======================\n")

if __name__ == "__main__":
    run_cli()
