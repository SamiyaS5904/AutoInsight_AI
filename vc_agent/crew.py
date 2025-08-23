from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Define Agent
agent = Agent(
    role="Helper",
    goal="Answer user questions politely",
    backstory="You are a helpful assistant who helps test CrewAI setup.",
    llm=llm
)

# Define Task
task = Task(
    description="Say hello to the user and confirm setup is working",
    expected_output="A friendly hello message confirming that CrewAI setup is working.",
    agent=agent
)

# Define Crew
crew = Crew(
    agents=[agent],
    tasks=[task]
)

# Run Crew
if __name__ == "__main__":
    result = crew.kickoff()
    print("\n✅ Crew result:\n", result)
