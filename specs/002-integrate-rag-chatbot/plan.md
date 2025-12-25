# Implementation Plan: Integrated RAG Chatbot

**Branch**: `002-integrate-rag-chatbot` | **Date**: 2025-12-16 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/002-integrate-rag-chatbot/spec.md`

## Summary

The objective is to integrate a Retrieval-Augmented Generation (RAG) chatbot into the Docusaurus book. The chatbot will answer user questions strictly based on the book's content, with modes for both full-book retrieval and answering based on user-selected text. The technical approach involves a FastAPI backend for orchestration, Cohere for embeddings, Qdrant for vector storage, OpenRouter for LLM routing, Neon Serverless Postgres for state, and a ChatKit SDK-based UI embedded in the frontend.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, Qdrant, Cohere, OpenRouter, OpenAI Agents/ChatKit SDK, Neon Postgres
**Storage**: Qdrant Cloud (Vector DB), Neon Serverless Postgres (Relational DB)
**Testing**: pytest
**Target Platform**: Web
**Project Type**: Web application
**Performance Goals**: p95 latency under 3 seconds for chat responses.
**Constraints**: Answers must be grounded in book content only.
**Scale/Scope**: To be determined, starting with the current book's content size.

## Constitution Check

*   **Spec-Kit Plus Origination**: PASS. The plan is derived from a spec.
*   **Docusaurus Documentation**: PASS. The chatbot is integrated into a Docusaurus site.
*   **Logical Hierarchy**: N/A for this feature.
*   **Verified Code Examples**: PASS. The RAG system will be tested to ensure correctness.
*   **GitHub Pages Deployment**: PASS. The final site will be deployable to GitHub Pages.
*   **Claude Code Assistance Guidelines**: N/A.

All gates pass.

## Project Structure

### Documentation (this feature)

```text
specs/002-integrate-rag-chatbot/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (not created by this command)
```

### Source Code (repository root)

```text
rag-chatbot-backend/
├── app/
│   ├── main.py
│   ├── core/
│   ├── apis/
│   ├── services/
│   └── models/
├── tests/
└── requirements.txt

my-book/
├── src/
│   ├── theme/
│   │   └── Root.js
│   └── components/
│       └── Chatbot.js
```

**Structure Decision**: A dedicated `rag-chatbot-backend` directory will be created for the Python-based backend, keeping it separate from the Docusaurus frontend (`my-book`). The frontend integration will be done by adding a new React component and modifying the Docusaurus root theme file.

## Complexity Tracking

No violations of the constitution were identified.