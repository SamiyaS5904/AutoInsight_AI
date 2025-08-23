from crewai import Agent, Crew, Task, Process
from crewai.llm import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()  # to load OPENAI_API_KEY from .env

# Define LLM (replace gpt-4 with your available model)
llm = OpenAI(model="gpt-4", api_key=os.getenv("OPENAI_API_KEY"))

# Define an Agent
researcher = Agent(
    role="Researcher",
    goal="Find useful information",
    backstory="You are great at researching things",
    llm=llm,
    verbose=True
)

# Define a Task
research_task = Task(
    description="Tell me a fun fact about space.",
    agent=researcher
)

# Create the Crew
crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    process=Process.sequential,
    verbose=True
)

# Run it
result = crew.kickoff()
print("Result:\n", result)
