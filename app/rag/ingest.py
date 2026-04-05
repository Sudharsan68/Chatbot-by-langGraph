from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from app.rag.qdrant_client import get_qdrant_client
from app.rag.embeddings import get_embeddings_model
from app.core.config import settings
from app.core.logging import setup_logger

logger = setup_logger(__name__)

def ingest_text(text: str, metadata: dict = None) -> int:
    """Splits text and ingests into Qdrant."""
    logger.info("Starting ingestion process...")
    
    # 1. Chunking
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    docs = [Document(page_content=chunk, metadata=metadata or {}) for chunk in chunks]
    
    # 2. Embedding + Vector Store
    embeddings = get_embeddings_model()
    
    qdrant_client = get_qdrant_client()
    vector_store = QdrantVectorStore(
        client=qdrant_client, 
        collection_name=settings.COLLECTION_NAME, 
        embedding=embeddings
    )
    
    vector_store.add_documents(docs)
    logger.info(f"Successfully ingested {len(docs)} chunks.")
    
    return len(docs)
