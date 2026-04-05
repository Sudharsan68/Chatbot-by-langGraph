from app.core.config import settings
from app.core.logging import setup_logger

logger = setup_logger(__name__)

def get_llm():
    """Returns an LLM instance based on the configured provider."""
    provider = settings.LLM_PROVIDER.lower()
    
    try:
        if provider == "openai":
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(model=settings.MODEL_NAME, temperature=0, openai_api_key=settings.OPENAI_API_KEY)
            
        elif provider == "groq":
            from langchain_groq import ChatGroq
            return ChatGroq(model=settings.MODEL_NAME, temperature=0, groq_api_key=settings.GROQ_API_KEY)
            
        elif provider == "ollama":
            from langchain_community.chat_models import ChatOllama
            return ChatOllama(model=settings.MODEL_NAME, base_url=settings.OLLAMA_BASE_URL, temperature=0)
            
        else:
            logger.warning(f"Unknown LLM provider {provider}, falling back to OpenAI.")
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    except ImportError as e:
        logger.error(f"Failed to import required provider package for {provider}. Make sure it is installed.")
        raise e
