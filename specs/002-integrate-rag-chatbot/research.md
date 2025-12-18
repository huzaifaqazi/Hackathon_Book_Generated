# Research: Integrated RAG Chatbot

This document records the key architectural and technical decisions for the RAG chatbot feature.

## 1. Embedding and Chunking Strategy

-   **Decision**: Content will be chunked by headings and semantic boundaries. The ideal chunk size and overlap will be determined during implementation to balance context richness and retrieval precision.
-   **Rationale**: Semantic chunking is more effective than fixed-size chunking as it keeps related content together, improving the quality of retrieval.
-   **Alternatives considered**: Fixed-size chunking. This was rejected because it can split related sentences or paragraphs, leading to incomplete context during retrieval.

## 2. Retrieval Parameters

-   **Decision**: The retrieval pipeline will fetch the top-k most relevant chunks from Qdrant. The value of 'k' will be tuned based on performance and context length limitations of the LLM. Metadata filters will be used to constrain searches where applicable.
-   **Rationale**: A configurable top-k allows for balancing retrieval speed and the amount of context provided to the LLM. Metadata filters are crucial for features like section-specific Q&A.
-   **Alternatives considered**: Retrieving all chunks above a certain similarity threshold. This was rejected as it could lead to an unpredictable number of chunks, potentially exceeding the LLM's context window.

## 3. LLM Routing via OpenRouter

-   **Decision**: OpenRouter will be used to route requests to the most appropriate LLM, balancing cost, performance, and quality. The specific model will be configurable.
-   **Rationale**: OpenRouter provides flexibility and allows for dynamic switching between different LLM providers without code changes. This is ideal for optimizing cost and performance.
-   **Alternatives considered**: Direct integration with a single LLM provider (e.g., OpenAI). This was rejected as it would lead to vendor lock-in and less flexibility.

## 4. Agent Design

-   **Decision**: A single, focused agent will be implemented using the OpenAI Agents SDK. The agent's primary role will be to synthesize answers from the retrieved context.
-   **Rationale**: A single agent is sufficient for the current scope. A tool-using agent would introduce unnecessary complexity.
-   **Alternatives considered**: A multi-agent system with separate agents for retrieval, and synthesis. This was deemed over-engineering for the current requirements.

## 5. Backend Architecture

-   **Decision**: A FastAPI backend will expose a RESTful API. Key endpoints will include `/chat` for handling user queries and `/ingest` for triggering the content ingestion process. Session state will be managed in Neon Postgres.
-   **Rationale**: FastAPI is a modern, high-performance Python web framework that is well-suited for building API-driven services.
-   **Alternatives considered**: Flask. FastAPI was chosen for its asynchronous capabilities and automatic OpenAPI documentation generation.

## 6. Frontend Integration

-   **Decision**: The chatbot will be integrated into the Docusaurus site using the ChatKit SDK. The UI will be placed in a consistent location on all pages, likely a floating action button.
-   **Rationale**: The ChatKit SDK provides a ready-to-use, customizable chat UI, accelerating frontend development.
-   **Alternatives considered**: Building a custom chat UI from scratch. This was rejected as it would be time-consuming and is not a core part of the feature.

## 7. Deployment and Scaling

-   **Decision**: The FastAPI backend will be containerized and deployed as a serverless function or container service. Qdrant Cloud and Neon Serverless Postgres are managed services that will scale automatically.
-   **Rationale**: A serverless architecture minimizes operational overhead and allows for a pay-per-use cost model.
-   **Alternatives considered**: Deploying to a dedicated virtual machine. This was rejected due to higher cost and maintenance overhead.
