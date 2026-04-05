from langgraph.graph import StateGraph, END
from app.graph.state import ChatbotState
from app.graph.nodes import (
    classify_intent_node,
    rag_retrieval_node,
    generate_rag_response_node,
    agent_action_node,
    generate_tool_response_node,
    fallback_node
)
from app.graph.router import route_by_intent

def build_graph() -> StateGraph:
    workflow = StateGraph(ChatbotState)
    
    # Add nodes
    workflow.add_node("classify_intent", classify_intent_node)
    workflow.add_node("rag_retrieval", rag_retrieval_node)
    workflow.add_node("generate_rag_response", generate_rag_response_node)
    workflow.add_node("agent_action", agent_action_node)
    workflow.add_node("generate_tool_response", generate_tool_response_node)
    workflow.add_node("fallback", fallback_node)
    
    # Add edges
    workflow.set_entry_point("classify_intent")
    
    workflow.add_conditional_edges(
        "classify_intent",
        route_by_intent,
        {
            "rag": "rag_retrieval",
            "action": "agent_action",
            "fallback": "fallback"
        }
    )
    
    workflow.add_edge("rag_retrieval", "generate_rag_response")
    workflow.add_edge("generate_rag_response", END)
    
    workflow.add_edge("agent_action", "generate_tool_response")
    workflow.add_edge("generate_tool_response", END)
    
    workflow.add_edge("fallback", END)
    
    return workflow.compile()

graph = build_graph()
