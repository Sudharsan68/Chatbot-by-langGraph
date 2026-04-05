from app.graph.state import ChatbotState

def route_by_intent(state: ChatbotState) -> str:
    """Routes based on the detected intent."""
    intent = state.get("detected_intent")
    if intent == "faq":
        return "rag"
    elif intent == "action":
        return "action"
    else:
        return "fallback"
