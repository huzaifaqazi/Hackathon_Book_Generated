# Task Breakdown: Integrated RAG Chatbot

**Branch**: `002-integrate-rag-chatbot` | **Date**: 2025-12-16
**Input**: `plan.md`, `spec.md`, `data-model.md`, `contracts/openapi.yaml`

This document breaks down the implementation of the RAG chatbot into actionable tasks, ordered by dependency.

## Phase 1: Project Setup

These tasks initialize the project structure for the backend service.

- [ ] T001 Create backend project structure in `rag-chatbot-backend/`.
- [ ] T002 Initialize a Python virtual environment in `rag-chatbot-backend/`.
- [ ] T003 Create `rag-chatbot-backend/requirements.txt` with initial dependencies (fastapi, uvicorn, python-dotenv, requests).
- [ ] T004 Create `rag-chatbot-backend/.env.example` file for environment variables.
- [ ] T005 Create basic FastAPI app structure in `rag-chatbot-backend/app/main.py`.

## Phase 2: Foundational/Core Pipeline

These tasks build the core ingestion and retrieval pipeline, which is a prerequisite for all user stories.

- [ ] T006 Implement sitemap parser to extract book URLs in `rag-chatbot-backend/app/services/ingestion.py`.
- [ ] T007 Implement content chunking logic in `rag-chatbot-backend/app/services/ingestion.py`.
- [ ] T008 [P] Set up Cohere client and embedding generation in `rag-chatbot-backend/app/services/embeddings.py`.
- [ ] T009 [P] Set up Qdrant client and vector store creation in `rag-chatbot-backend/app/services/vector_store.py`.
- [ ] T010 Implement the `/ingest` endpoint in `rag-chatbot-backend/app/apis/ingestion_api.py`.
- [ ] T011 [P] Set up Neon Postgres connection and session/log table schemas in `rag-chatbot-backend/app/core/db.py`.
- [ ] T012 [P] Set up OpenRouter client for LLM interaction in `rag-chatbot-backend/app/services/llm.py`.

## Phase 3: User Story 1 (P1) - Full-Book Chat

**Goal**: As a reader, I want to ask a question in natural language and receive an answer based on the full content of the book.
**Independent Test**: Can be tested by asking a question and verifying the answer is accurate and cites sources from the book.

- [ ] T013 [US1] Implement retrieval logic to get relevant chunks from Qdrant in `rag-chatbot-backend/app/services/retrieval.py`.
- [ ] T014 [US1] Implement agent prompt construction with retrieved context in `rag-chatbot-backend/app/services/agent.py`.
- [ ] T015 [US1] Implement `/chat` endpoint logic for full-book questions in `rag-chatbot-backend/app/apis/chat_api.py`.
- [ ] T016 [P] [US1] Create basic Chatbot UI component in `my-book/src/components/Chatbot.js`.
- [ ] T017 [P] [US1] Add the Chatbot component to the Docusaurus site in `my-book/src/theme/Root.js`.
- [ ] T018 [US1] Implement frontend logic to call the `/chat` endpoint in `my-book/src/components/Chatbot.js`.

## Phase 4: User Story 2 (P2) - Selected-Text Chat

**Goal**: As a reader, I want to highlight a section of text and ask a follow-up question about it.
**Independent Test**: Can be tested by selecting text, asking a question, and verifying the answer is based on the selection.

- [ ] T019 [US2] Update `/chat` endpoint to handle `selected_text` in the request in `rag-chatbot-backend/app/apis/chat_api.py`.
- [ ] T020 [US2] Implement agent logic to prioritize `selected_text` when available in `rag-chatbot-backend/app/services/agent.py`.
- [ ] T021 [P] [US2] Implement frontend logic to get selected text and send it with the query in `my-book/src/components/Chatbot.js`.

## Phase 5: User Story 3 (P3) - Source Navigation

**Goal**: As a reader, I want to click on the source citations in the chatbot's answer to navigate to the relevant part of the book.
**Independent Test**: Can be tested by clicking a citation link and verifying it navigates to the correct section.

- [ ] T022 [US3] Ensure source metadata (URL, heading) is returned from the `/chat` endpoint in `rag-chatbot-backend/app/apis/chat_api.py`.
- [ ] T023 [P] [US3] Implement frontend logic to display sources as clickable links in `my-book/src/components/Chatbot.js`.

## Phase 6: Polish & Cross-Cutting Concerns

- [ ] T024 [P] Add comprehensive error handling to the backend API.
- [ ] T025 [P] Implement logging for all backend services.
- [ ] T026 [P] Write unit tests for critical backend components (ingestion, retrieval, agent).
- [ ] T027 [P] Add clear API documentation using OpenAPI.
- [ ] T028 Create a `README.md` for the `rag-chatbot-backend` directory.

## Dependencies

- **User Story 1** is foundational.
- **User Story 2** depends on **User Story 1**.
- **User Story 3** depends on **User Story 1**.

## Parallel Execution

- Within each user story phase, backend and frontend tasks marked with **[P]** can be worked on in parallel.
- The Foundational phase has several parallelizable tasks for setting up different clients (Cohere, Qdrant, Neon, OpenRouter).

## Implementation Strategy

The implementation will follow an MVP-first approach. The initial focus will be on completing all tasks for **User Story 1** to deliver the core chat functionality. Subsequent user stories will be implemented as incremental enhancements.
