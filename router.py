# src/vc_agent/router.py

def route_query(user_input: str):
    """
    Route user queries to the correct agent based on keywords.
    """
    user_input = user_input.lower()

    if "compare" in user_input:
        return "comparison"
    elif "price" in user_input or "features" in user_input:
        return "discussion"
    elif "google" in user_input or "search" in user_input:
        return "google_search"
    else:
        return "discussion"  # default fallback
