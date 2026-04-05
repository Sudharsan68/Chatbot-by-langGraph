from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Student Support AI Chatbot"
    VERSION: str = "1.0.0"
    
    # LLM config
    LLM_PROVIDER: str = "groq" # "openai", "groq", "ollama"
    OPENAI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    MODEL_NAME: str = "llama-3.1-8b-instant"
    
    # Vector DB
    QDRANT_URL: str = ":memory:" # Use ":memory:" for local, or actual URL
    QDRANT_API_KEY: str = ""
    COLLECTION_NAME: str = "support_docs"

    class Config:
        env_file = ".env"

settings = Settings()
