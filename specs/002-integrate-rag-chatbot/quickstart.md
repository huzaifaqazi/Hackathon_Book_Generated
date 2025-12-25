# Quickstart: Integrated RAG Chatbot

This guide provides instructions to set up and run the RAG chatbot locally.

## Prerequisites

-   Python 3.11+
-   Node.js and npm (for the Docusaurus site)
-   Access to Qdrant Cloud, Neon, and Cohere API keys.

## Backend Setup

1.  **Navigate to the backend directory**:
    ```bash
    cd rag-chatbot-backend
    ```

2.  **Create a virtual environment and install dependencies**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Set up environment variables**:
    Create a `.env` file in the `rag-chatbot-backend` directory and add the following:
    ```
    QDRANT_API_KEY="..."
    NEON_DATABASE_URL="..."
    COHERE_API_KEY="..."
    OPENROUTER_API_KEY="..."
    ```

4.  **Run the backend server**:
    ```bash
    uvicorn app.main:app --reload
    ```
    The API will be available at `http://localhost:8000`.

## Frontend Setup

1.  **Navigate to the frontend directory**:
    ```bash
    cd my-book
    ```

2.  **Install dependencies**:
    ```bash
    npm install
    ```

3.  **Run the Docusaurus development server**:
    ```bash
    npm start
    ```
    The book will be available at `http://localhost:3000`. The chatbot UI will be integrated into the site.

## Ingestion

To populate the vector database, send a POST request to the `/ingest` endpoint:

```bash
curl -X POST http://localhost:8000/ingest
```
