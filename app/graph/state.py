from typing import TypedDict, List, Optional, Any, Dict
from langchain_core.documents import Document

class ChatbotState(TypedDict):
    session_id: str
    user_query: str
    chat_history: List[Dict[str, str]]
    
    # Graph execution state
    detected_intent: Optional[str]
    retrieved_docs: Optional[List[Document]]
    tool_result: Optional[str]
    final_answer: Optional[str]
