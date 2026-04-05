from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ChatRequest(BaseModel):
    session_id: str
    query: str

class ChatResponse(BaseModel):
    session_id: str
    answer: str
    intent: str
    sources: Optional[List[Dict[str, Any]]] = None

class IngestRequest(BaseModel):
    text: str
    metadata: Optional[Dict[str, Any]] = None

class IngestResponse(BaseModel):
    status: str
    chunks_processed: int
