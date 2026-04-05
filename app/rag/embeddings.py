from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.embeddings import Embeddings

# Singleton for embedding model to avoid reloading/reconnecting
_embeddings_model = None

def get_embeddings_model() -> Embeddings:
    global _embeddings_model
    if _embeddings_model is None:
        # Use local_files_only=False first to download, then it uses cache
        _embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return _embeddings_model
