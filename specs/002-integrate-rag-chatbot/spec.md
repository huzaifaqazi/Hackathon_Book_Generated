# Feature Specification: Integrated RAG Chatbot

**Feature Branch**: `002-integrate-rag-chatbot`  
**Created**: 2025-12-16
**Status**: Draft  
**Input**: User description: "System: Integrated RAG Chatbot for Docusaurus Book Context: - Phase 2 objective: Integrate a Retrieval-Augmented Generation (RAG) chatbot into the published book. Goal: - Build and embed a content-grounded RAG chatbot that answers user questions strictly from the book, including a mode that answers using only user-selected text. Core Technologies: - LLM routing: OpenRouter - Embeddings: Cohere - Vector database: Qdrant Cloud (Free Tier) - Agent framework: OpenAI Agents / ChatKit SDKs - Backend: FastAPI - Relational store: Neon Serverless Postgres - Frontend: Embedded chatbot UI inside Docusaurus Functional Specification: 1. Content Ingestion & Indexing - Extract all book pages via sitemap.xml. - Clean and normalize content for retrieval. - Chunk content by headings and semantic boundaries. - Generate embeddings using Cohere. - Store vectors and metadata (URL, section, heading) in Qdrant. 2. Retrieval Pipeline - Embed user queries using Cohere. - Perform semantic search over Qdrant. - Retrieve top-k relevant chunks with metadata. - Support two modes: - Full-book retrieval - Selected-text-only answering (bypass vector search) 3. Agent & Reasoning Layer - Implement an agent using OpenAI Agents SDK via OpenRouter. - Inject retrieved context into the agent prompt. - Enforce constraints: - Answers must be grounded in retrieved or selected text only - No external knowledge or hallucination - Return answers with source references. 4. Backend Orchestration - Build a FastAPI service to coordinate: - Query handling - Embedding and retrieval - Agent execution - Use Neon Postgres for session state, query logs, and metadata. - Expose secure API endpoints for the frontend. 5. Frontend Integration - Embed the chatbot in Docusaurus using ChatKit SDK. - Pass page context and optional user-selected text to backend. - Display responses with citations and section links. Success Criteria: - Chatbot answers accurately from book content only. - Selected-text-only mode works reliably. - End-to-end latency is acceptable for interactive use. - Chatbot is accessible on all book pages."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ask questions about the book (Priority: P1)

As a reader, I want to ask a question in natural language and receive an answer based on the full content of the book, so I can find information quickly without manual searching.

**Why this priority**: This is the core functionality of the RAG chatbot and provides the primary value to the user.

**Independent Test**: Can be tested by asking a question that can be answered from the book's content and verifying that the answer is accurate and relevant.

**Acceptance Scenarios**:

1. **Given** a user is on any page of the book, **When** they open the chatbot and ask "What is ROS2?", **Then** they receive a concise answer summarizing the introduction to ROS2 from the book.
2. **Given** a user asks a question, **When** the answer is generated, **Then** the response includes citations linking to the relevant book sections.

---

### User Story 2 - Ask questions about selected text (Priority: P2)

As a reader, I want to highlight a section of text and ask a follow-up question about it, so I can get a specific answer grounded in the context I've provided.

**Why this priority**: This enhances the user experience by allowing for more focused and contextual inquiries.

**Independent Test**: Can be tested by selecting a paragraph, opening the chatbot, and asking a question specific to that paragraph.

**Acceptance Scenarios**:

1. **Given** a user has selected a paragraph about URDF modeling, **When** they ask the chatbot "what is this for?", **Then** they receive an answer explaining the purpose of URDF based *only* on the selected text.

---

### User Story 3 - Navigate to source (Priority: P3)

As a reader, I want to click on the source citations in the chatbot's answer, so I can easily navigate to the relevant part of the book for more details.

**Why this priority**: This provides transparency and allows users to dig deeper into the topics they are interested in.

**Independent Test**: Can be tested by asking a question, receiving an answer with citations, and clicking on a citation link.

**Acceptance Scenarios**:

1. **Given** a chatbot answer with a citation, **When** the user clicks the citation link, **Then** the page scrolls to the corresponding section in the book.

---

### Edge Cases

- **Out-of-scope questions**: When a user asks a question unrelated to the book's content, the chatbot should respond with a message like, "I can only answer questions about the content of this book."
- **No answer found**: When the book does not contain information to answer a user's question, the chatbot should state that it could not find a relevant answer.
- **Ambiguous questions**: When a user's question is too vague, the chatbot may ask for clarification.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST extract and process all content from the Docusaurus site's `sitemap.xml`.
- **FR-002**: The system MUST clean and chunk the content by headings and semantic boundaries for efficient retrieval.
- **FR-003**: The system MUST generate embeddings for content chunks using Cohere.
- **FR-004**: The system MUST store the vectors and associated metadata (URL, section, heading) in a Qdrant Cloud vector database.
- **FR-005**: The system MUST embed user queries using Cohere.
- **FR-006**: The system MUST perform semantic search on the Qdrant database to find relevant content.
- **FR-007**: The system MUST support two retrieval modes: full-book and selected-text-only.
- **FR-008**: The agent MUST formulate answers grounded *only* in the retrieved or selected text context.
- **FR-009**: The system MUST NOT use external knowledge or hallucinate information.
- **FR-010**: The system MUST return answers with citations and links to the source sections in the book.
- **FR-011**: A FastAPI backend MUST be implemented to orchestrate the entire RAG pipeline.
- **FR-012**: The system MUST use Neon Serverless Postgres for managing session state, query logs, and other metadata.
- **FR-013**: A chatbot UI, built with the ChatKit SDK, MUST be embedded in the Docusaurus frontend.
- **FR-014**: The frontend MUST be able to pass page context and optional user-selected text to the backend.

### Key Entities

- **Content Chunk**: A segment of text extracted from the book, associated with metadata such as its source URL, section heading, and original content.
- **Vector Embedding**: The numerical, multi-dimensional representation of a content chunk or a user query, generated by the Cohere model.
- **Chat Session**: Represents a single, stateful conversation between a user and the chatbot, including conversation history.
- **Query Log**: A record stored in the Postgres database containing a user's query, the retrieved documents, and the final generated response.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: At least 95% of the chatbot's answers must be factually consistent with the book's content, as verified by manual review of a sample set of questions.
- **SC-002**: The "selected-text-only" mode must correctly use only the provided context for 99% of queries in a test set.
- **SC-003**: The end-to-end p95 latency for a chatbot query (from submitting the question to displaying the answer) must be under 3 seconds.
- **SC-004**: The chatbot UI element must be successfully rendered and accessible on all pages of the Docusaurus book.
- **SC-005**: All generated answers that are based on book content must include at least one valid source citation with a functioning link to the relevant section.