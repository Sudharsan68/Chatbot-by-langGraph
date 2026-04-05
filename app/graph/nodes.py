from app.graph.state import ChatbotState
from app.llm.provider import get_llm
from app.llm.prompts import INTENT_PROMPT, QA_PROMPT, FALLBACK_PROMPT
from app.rag.retriever import retrieve_docs
from app.tools.support_tools import check_class_schedule, reschedule_class, create_support_ticket
from app.utils.helpers import format_docs
from langchain_core.messages import HumanMessage, SystemMessage

llm = get_llm()

def classify_intent_node(state: ChatbotState) -> ChatbotState:
    """Classifies the intent of the user query."""
    prompt = INTENT_PROMPT.format(query=state["user_query"])
    response = llm.invoke(prompt)
    intent = response.content.strip().lower()
    
    if "faq" in intent:
        intent = "faq"
    elif "action" in intent:
        intent = "action"
    else:
        intent = "unclear"
        
    return {"detected_intent": intent}

def rag_retrieval_node(state: ChatbotState) -> ChatbotState:
    """Retrieves documents for FAQ questions."""
    docs = retrieve_docs(state["user_query"])
    return {"retrieved_docs": docs}

def generate_rag_response_node(state: ChatbotState) -> ChatbotState:
    """Generates the final answer using retrieved docs."""
    docs = state.get("retrieved_docs", [])
    context = format_docs(docs)
    
    prompt = QA_PROMPT.format(context=context, query=state["user_query"])
    response = llm.invoke(prompt)
    
    return {"final_answer": response.content}

def agent_action_node(state: ChatbotState) -> ChatbotState:
    """Handles tool calling."""
    from app.tools.support_tools import TOOLS
    llm_with_tools = llm.bind_tools(TOOLS)
    
    # Build conversational payload to allow the LLM to choose the right tool using previous context
    messages = [SystemMessage(content="You are a helpful assistant with tools.")]
    for msg in state.get("chat_history", []):
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(SystemMessage(content=msg["content"]))
            
    messages.append(HumanMessage(content=state["user_query"]))
    
    response = llm_with_tools.invoke(messages)
    
    if hasattr(response, "tool_calls") and response.tool_calls:
        # Just running the first tool for demonstration purposes
        tool_call = response.tool_calls[0]
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        
        tool_res = ""
        if tool_name == "check_class_schedule":
            tool_res = check_class_schedule.invoke(tool_args)
        elif tool_name == "reschedule_class":
            tool_res = reschedule_class.invoke(tool_args)
        elif tool_name == "create_support_ticket":
            tool_res = create_support_ticket.invoke(tool_args)
            
        return {"tool_result": str(tool_res)}
    
    return {"tool_result": "I am not sure which tool to use."}

def generate_tool_response_node(state: ChatbotState) -> ChatbotState:
    """Generates a conversational response after a tool call."""
    tool_res = state.get("tool_result", "")
    prompt = f"The user asked: '{state['user_query']}'. The system performed an action and the result is: '{tool_res}'. Please relay this result accurately and politely to the user."
    response = llm.invoke(prompt)
    return {"final_answer": response.content}

def fallback_node(state: ChatbotState) -> ChatbotState:
    """Handles unclear or unrelated queries."""
    prompt = FALLBACK_PROMPT.format(query=state["user_query"])
    response = llm.invoke(prompt)
    return {"final_answer": response.content}
