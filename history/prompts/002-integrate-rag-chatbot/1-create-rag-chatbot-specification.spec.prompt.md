---
id: 1
title: Create RAG Chatbot Specification
stage: spec
date: 2025-12-16
surface: agent
model: gemini-pro
feature: 002-integrate-rag-chatbot
branch: 002-integrate-rag-chatbot
user: "system"
command: "/sp.specify"
labels: ["rag", "chatbot", "docusaurus"]
links:
  spec: "specs/002-integrate-rag-chatbot/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/002-integrate-rag-chatbot/spec.md"
  - "specs/002-integrate-rag-chatbot/checklists/requirements.md"
tests:
  - "None"
---

## Prompt

System: Integrated RAG Chatbot for Docusaurus Book Context: - Phase 2 objective: Integrate a Retrieval-Augmented Generation (RAG) chatbot into the published book. Goal: - Build and embed a content-grounded RAG chatbot that answers user questions strictly from the book, including a mode that answers using only user-selected text. Core Technologies: - LLM routing: OpenRouter - Embeddings: Cohere - Vector database: Qdrant Cloud (Free Tier) - Agent framework: OpenAI Agents / ChatKit SDKs - Backend: FastAPI - Relational store: Neon Serverless Postgres - Frontend: Embedded chatbot UI inside Docusaurus Functional Specification: 1. Content Ingestion & Indexing - Extract all book pages via `sitemap.xml`. - Clean and normalize content for retrieval. - Chunk content by headings and semantic boundaries. - Generate embeddings using Cohere. - Store vectors and metadata (URL, section, heading) in Qdrant. 2. Retrieval Pipeline - Embed user queries using Cohere. - Perform semantic search over Qdrant. - Retrieve top-k relevant chunks with metadata. - Support two modes: - Full-book retrieval - Selected-text-only answering (bypass vector search) 3. Agent & Reasoning Layer - Implement an agent using OpenAI Agents SDK via OpenRouter. - Inject retrieved context into the agent prompt. - Enforce constraints: - Answers must be grounded in retrieved or selected text only - No external knowledge or hallucination - Return answers with source references. 4. Backend Orchestration - Build a FastAPI service to coordinate: - Query handling - Embedding and retrieval - Agent execution - Use Neon Postgres for session state, query logs, and metadata. - Expose secure API endpoints for the frontend. 5. Frontend Integration - Embed the chatbot in Docusaurus using ChatKit SDK. - Pass page context and optional user-selected text to backend. - Display responses with citations and section links. Success Criteria: - Chatbot answers accurately from book content only. - Selected-text-only mode works reliably. - End-to-end latency is acceptable for interactive use. - Chatbot is accessible on all book pages.

## Response snapshot

I have created the feature specification for the RAG chatbot, including the `spec.md` file and the `requirements.md` checklist. The feature is ready for the planning phase.

## Outcome

- ✅ Impact: The feature specification has been successfully created, defining the scope and requirements for the RAG chatbot.
- 🧪 Tests: No tests were run.
- 📁 Files: 
  - `specs/002-integrate-rag-chatbot/spec.md`
  - `specs/002-integrate-rag-chatbot/checklists/requirements.md`
- 🔁 Next prompts: `/sp.plan`
- 🧠 Reflection: The `create-new-feature.ps1` script failed, but I was able to recover by manually creating the spec file and checklist. I should be more careful about the script's arguments in the future.

## Evaluation notes (flywheel)

- Failure modes observed: The powershell script for feature creation is brittle and failed due to argument parsing.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
