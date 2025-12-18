# RAG Chatbot Backend

This is the FastAPI backend for the Docusaurus RAG Chatbot. It handles content ingestion, embedding generation, vector storage, LLM interaction, and chat session management.

## Setup

1.  **Clone the repository (if you haven't already)**:
    ```bash
    git clone <your-repo-url>
    cd rag-chatbot-backend
    ```

2.  **Create a virtual environment and activate it**:
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables**:
    Create a `.env` file in this directory with your API keys and database URL:
    ```
    QDRANT_API_KEY=your_qdrant_api_key
    QDRANT_HOST=your_qdrant_host_url # e.g., 'https://[cluster-url].qdrant.tech'
    NEON_DATABASE_URL=your_neon_postgres_connection_string
    COHERE_API_KEY=your_cohere_api_key
    OPENROUTER_API_KEY=your_openrouter_api_key
    OPENROUTER_MODEL=openai/gpt-3.5-turbo # or another model from OpenRouter
    ```

5.  **Run the FastAPI application**:
    ```bash
    uvicorn app.main:app --reload
    ```
    The API will be available at `http://localhost:8000`. OpenAPI documentation can be accessed at `http://localhost:8000/docs`.

## API Endpoints

-   **`POST /api/v1/ingest`**: Triggers content ingestion from the Docusaurus sitemap.
-   **`POST /api/v1/chat`**: Sends a query to the RAG chatbot and receives a response.

## Database Migrations

Database tables are automatically created on application startup if they don't exist.
