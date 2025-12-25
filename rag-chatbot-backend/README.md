# RAG Chatbot Backend

This directory contains the Python-based backend for the RAG chatbot. It is a FastAPI application that provides a RESTful API for the chatbot frontend.

## Setup

1.  **Create a virtual environment and install dependencies**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

2.  **Set up environment variables**:
    Create a `.env` file in this directory and add the following:
    ```
    QDRANT_API_KEY="..."
    QDRANT_HOST="..."
    NEON_DATABASE_URL="..."
    COHERE_API_KEY="..."
    OPENROUTER_API_KEY="..."
    ```

3.  **Run the backend server**:
    ```bash
    uvicorn app.main:app --reload
    ```
    The API will be available at `http://localhost:8000`. You can access the Swagger UI at `http://localhost:8000/docs`.

## Ingestion

To populate the vector database with the content from the book, send a POST request to the `/api/v1/ingest` endpoint:

```bash
curl -X POST http://localhost:8000/api/v1/ingest
```