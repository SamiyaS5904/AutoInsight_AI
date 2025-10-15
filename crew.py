from dotenv import load_dotenv
import os
import openai
import requests
import traceback

# --- Load environment variables from .env ---
load_dotenv()  # <-- this reads your .env file

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
MODEL_NAME = os.getenv("MODEL", "gpt-4o-mini")

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

SYSTEM_PROMPT = (
    "You are AutoInsight AI, a comprehensive automotive expert. "
    "Your task is to answer user queries using real-time information from Google Search grounding. "
    "If the user asks for a comparison, structure the main part of your response as a clear markdown table. "
    "For all other questions, provide a friendly, factual, and detailed explanation."
)

# --- Serper search function ---
def perform_serper_search(query: str, num_results=3):
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {"q": query, "num": num_results}
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        results = [{"title": item.get("title"), "link": item.get("link")} for item in data.get("organic", [])]
        return results
    except Exception as e:
        print(f"Serper search error: {e}")
        return []

# --- Main AI function ---
def kickoff_crew_ai(user_input: str):
    print(f"\n--- [Step 1] User Input: {user_input}")
    search_results = perform_serper_search(user_input)
    
    search_context = ""
    if search_results:
        search_context = "Here are some recent sources for reference:\n"
        for i, item in enumerate(search_results, 1):
            search_context += f"* [{item['title']}]({item['link']})\n"

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"{user_input}\n\n{search_context}"}
    ]

    try:
        response = openai.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        # ✅ Fixed here: access message content correctly
        if response.choices and len(response.choices) > 0:
            generated_text = response.choices[0].message.content
        else:
            generated_text = "⚠️ No response returned from the AI model."
    except Exception:
        generated_text = f"CRITICAL API/NETWORK ERROR: {traceback.format_exc()}"

    sources_markdown = ""
    if search_results:
        sources_markdown = "\n\n---\n**🔍 Sources Used:**\n"
        for item in search_results:
            sources_markdown += f"* [{item['title']}]({item['link']})\n"

    return generated_text + sources_markdown

# --- Example usage ---
if __name__ == "__main__":
    user_query = input("Ask AutoInsight AI: ")
    answer = kickoff_crew_ai(user_query)
    print("\n--- AI Response ---\n")
    print(answer)
