from langchain_qdrant import QdrantVectorStore
from app.rag.qdrant_client import get_qdrant_client
from app.rag.embeddings import get_embeddings_model
from app.core.config import settings
from typing import List
from langchain_core.documents import Document

def retrieve_docs(query: str, top_k: int = 3) -> List[Document]:
    """Retrieve documents using similarity search."""
    embeddings = get_embeddings_model()
    client = get_qdrant_client()
    vector_store = QdrantVectorStore(
        client=client, 
        collection_name=settings.COLLECTION_NAME, 
        embedding=embeddings
    )
    results = vector_store.similarity_search(query, k=top_k)
    return results
