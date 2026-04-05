from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from app.core.config import settings
from app.core.logging import setup_logger

logger = setup_logger(__name__)

def get_qdrant_client() -> QdrantClient:
    # Forced to local disk path 'qdrant_data' to bypass your PC's network DNS errors
    return QdrantClient(path="qdrant_data")

def init_collection(embedding_size: int = 384): # Updated for HuggingFace
    client = get_qdrant_client()
    try:
        collections = client.get_collections().collections
        exists = any(c.name == settings.COLLECTION_NAME for c in collections)
        if not exists:
            client.create_collection(
                collection_name=settings.COLLECTION_NAME,
                vectors_config=VectorParams(size=embedding_size, distance=Distance.COSINE),
            )
            logger.info(f"Created collection {settings.COLLECTION_NAME}")
    except Exception as e:
        logger.error(f"Error initializing Qdrant collection: {e}")

