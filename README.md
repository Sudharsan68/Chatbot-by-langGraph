# AI Agentic Support System

An enterprise-ready AI chatbot architecture engineered for customer support and educational platform assistance. The system combines deterministic graph-based routing with Retrieval-Augmented Generation (RAG) and dynamic tool-calling to resolve complex multi-step user inquiries.

Designed for high performance and scalability, the backend supports both local and **Cloud Qdrant** vector storage. It utilizes on-device HuggingFace embedding models and Groq's lightning-fast Llama 3.1 inference engine.

---

## 🚀 Core Capabilities

- **Graph-Based Orchestration (LangGraph):** Employs explicit conditional routing to classify intents. Requests are deterministically directed to a knowledge-retrieval pipeline, an agentic tool executor, or a predefined fallback handler.
- **Hybrid RAG Pipeline (Qdrant + HuggingFace):** Supports in-memory, local-disk, or **Cloud Qdrant** connectivity. Generates embeddings mathematically 100% offline via the `all-MiniLM-L6-v2` model, significantly reducing API costs and latency.
- **Dynamic File Ingestion:** Features native PDF parsing. Uploaded documents are automatically buffered, extracted via `pypdf`, dynamically chunked, embedded, and mapped to the Qdrant vector space.
- **LLM Tool Execution:** Natively supports multi-tool selection, enabling the LLM to trigger backend APIs (such as checking schedules or creating support tickets) before summarizing an answer.
- **High-Concurrency API (FastAPI):** Deploys as a lightweight, asynchronous API server, ready to be consumed by modern React, Vue, or Next.js frontends.

---

## 🏗 Architecture

```mermaid
graph TD;
    UserQuery["User Query"] --> |POST /chat| IntentRouter["Intent Router (LangGraph Classifier)"];
    
    IntentRouter -->|faq| RAG["RAG Retrieval Engine (Cloud Qdrant)"];
    IntentRouter -->|action| Agent["Agentic Tool Engine"];
    IntentRouter -->|unclear| Fallback["Standard LLM Fallback"];
    
    RAG --> Response["Generation (Llama 3.1 via Groq)"];
    Agent --> Response;
    Fallback --> Response;
    
    Response --> UserResponse["Final Answer Delivery"];
```

---

## 📋 Installation

### 1. Environment Setup
Configure your virtual environment and install the required dependencies:
```bash
# Initialize virtual environment
python -m venv .venv

# Activate on Windows:
.venv\Scripts\activate
# Activate on MacOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
Create a `.env` file from the example template. You will need a **Groq API Key** and your **Qdrant Cloud Credentials**.
```bash
cp .env.example .env
```
Ensure your `.env` variables contain the following fundamentals:
```env
# Core Configuration
LLM_PROVIDER="groq"
MODEL_NAME="llama-3.1-8b-instant"
GROQ_API_KEY="your-groq-api-key"

# Vector Database (Cloud)
QDRANT_URL="https://your-qdrant-cloud-url"
QDRANT_API_KEY="your-qdrant-api-key"
COLLECTION_NAME="support_docs_v2"
```

---

## ⚙️ Execution & Deployment

Start the asynchronous API server:
```bash
python run.py
```
By default, the server runs on `http://127.0.0.1:8000`. 
To explore and execute endpoints visually, navigate to the Swagger UI playground at **`http://127.0.0.1:8000/docs`**.

---

## 📡 API Reference

### Uploading Documentation (PDF)
Extracts and ingests policies and knowledge directly into the cloud vector store.
```bash
curl -X POST "http://127.0.0.1:8000/ingest-pdf" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@knowledge-base.pdf"
```

### Chat Completion (Knowledge Retrieval)
Queries the system using standard conversational retrieval.
```bash
curl -X POST http://127.0.0.1:8000/chat \
-H "Content-Type: application/json" \
-d '{
    "session_id": "session_8892",
    "query": "How do I get a refund for a missed class?"
}'
```
