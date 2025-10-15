from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()  # .env file load karega
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
response = llm.invoke("Hello, test message from CrewAI setup.")
print(response)
