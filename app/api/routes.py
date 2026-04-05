from fastapi import APIRouter, HTTPException, UploadFile, File
from app.schemas.models import ChatRequest, ChatResponse, IngestRequest, IngestResponse
from app.graph.workflow import graph
from app.memory.session_store import session_store
from app.rag.ingest import ingest_text
from app.core.logging import setup_logger

logger = setup_logger(__name__)
router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    logger.info(f"Received query for session {request.session_id}: {request.query}")
    
    history = session_store.get_history(request.session_id)
    
    initial_state = {
        "session_id": request.session_id,
        "user_query": request.query,
        "chat_history": history,
        "detected_intent": None,
        "retrieved_docs": None,
        "tool_result": None,
        "final_answer": None
    }
    
    try:
        # Run graph
        final_state = graph.invoke(initial_state)
        
        answer = final_state.get("final_answer", "Sorry, I had an issue processing your request.")
        intent = final_state.get("detected_intent", "unknown")
        
        # Parse sources properly to handle un-serializable components
        sources = []
        if final_state.get("retrieved_docs"):
            sources = [{"page_content": doc.page_content, "metadata": doc.metadata} for doc in final_state["retrieved_docs"]]
            
        # Update session memory
        session_store.add_message(request.session_id, "user", request.query)
        session_store.add_message(request.session_id, "assistant", answer)
        
        return ChatResponse(
            session_id=request.session_id,
            answer=answer,
            intent=intent,
            sources=sources
        )
    except Exception as e:
        logger.error(f"Error processing chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ingest", response_model=IngestResponse)
async def ingest(request: IngestRequest):
    try:
        count = ingest_text(request.text, request.metadata)
        return IngestResponse(status="success", chunks_processed=count)
    except Exception as e:
        logger.error(f"Error ingesting documentation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ingest-pdf", response_model=IngestResponse)
async def ingest_pdf(file: UploadFile = File(...)):
    """Accepts a PDF file upload, extracts text, and ingests it."""
    try:
        import os
        from langchain_community.document_loaders import PyPDFLoader
        import uuid
        
        # Read the file first
        content = await file.read()
        if not content:
            raise ValueError("The uploaded PDF file is completely empty.")
            
        # Create a safe, unique temp file path
        tmp_path = f"temp_{uuid.uuid4().hex}.pdf"
        
        # Save uploaded file to temp location explicitly using standard open
        with open(tmp_path, "wb") as f:
            f.write(content)
            
        try:
            loader = PyPDFLoader(tmp_path)
            docs = loader.load()
            if not docs:
                raise ValueError("Could not extract any text from the PDF.")
                
            text = "\n".join([doc.page_content for doc in docs])
            count = ingest_text(text, {"source": file.filename})
            return IngestResponse(status="success", chunks_processed=count)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
                
    except Exception as e:
        logger.error(f"Error ingesting PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health():
    return {"status": "ok"}
