from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from app.core.config import settings
from app.core.logging import setup_logger

logger = setup_logger(__name__)

def get_qdrant_client() -> QdrantClient:
    url = settings.QDRANT_URL
    api_key = settings.QDRANT_API_KEY if settings.QDRANT_API_KEY else None
    
    if url == ":memory:" or url.startswith("./") or url.endswith(".db"):
        logger.info("Connecting to local Qdrant storage")
        return QdrantClient(path="qdrant_data")
    else:
        logger.info(f"Connecting to Cloud Qdrant at {url}")
        return QdrantClient(url=url, api_key=api_key)

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

