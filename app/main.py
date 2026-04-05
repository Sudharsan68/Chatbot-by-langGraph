from fastapi import FastAPI
from app.api.routes import router
from app.core.config import settings
from app.rag.qdrant_client import init_collection
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Student Support AI Chatbot utilizing LangGraph, Qdrant, and flexible LLMs."
)

@app.on_event("startup")
def on_startup():
    init_collection()

app.include_router(router)
