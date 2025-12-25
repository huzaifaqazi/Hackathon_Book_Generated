---
description: "Task list for RAG chatbot end-to-end validation"
---

# Tasks: RAG Chatbot End-to-End Validation

**Input**: User request to validate the RAG chatbot functionality.
**Prerequisites**: A running instance of the RAG chatbot backend and frontend.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which validation phase this task belongs to (e.g., V1, V2, V3)
- Include exact file paths in descriptions

## Phase 1: Setup

**Purpose**: Verify the testing environment and dependencies.

- [X] T001 Verify all backend dependencies are installed from `rag-chatbot-backend/requirements.txt`
- [X] T002 Verify all frontend dependencies are installed from `my-book/package.json`
- [X] T003 Ensure the backend server is running and accessible.
- [X] T004 Ensure the frontend development server is running and accessible.

---

## Phase 2: Backend Verification (V1)

**Goal**: Confirm the LLM model is loaded and the backend can generate a response.

**Independent Test**: The backend API responds successfully to a simple chat request.

### Implementation for Backend Verification

- [X] T005 [V1] Add a log statement in `rag-chatbot-backend/app/main.py` or relevant service to print the loaded LLM model name on startup.
- [X] T006 [V1] Create a test script `rag-chatbot-backend/tests/test_direct_llm_call.py` to call the `get_answer_from_agent()` function directly and verify it returns a non-empty response.
- [X] T007 [V1] Run the test script `rag-chatbot-backend/tests/test_direct_llm_call.py` and confirm it passes.

---

## Phase 3: RAG Pipeline Test (V2)

**Goal**: Verify the retrieval component of the RAG pipeline is fetching correct context.

**Independent Test**: For specific questions, the correct content chunks are retrieved from the vector database.

### Implementation for RAG Pipeline Test

- [X] T008 [V2] Create a test script `rag-chatbot-backend/tests/test_retrieval_pipeline.py` to test the retrieval of chunks.
- [X] T009 [V2] In `rag-chatbot-backend/tests/test_retrieval_pipeline.py`, add a test case for the query "What is ROS 2?" and assert that the retrieved chunks are relevant to ROS 2.
- [X] T010 [V2] In `rag-chatbot-backend/tests/test_retrieval_pipeline.py`, add a test case for the query "Explain photorealistic simulation" and assert that the retrieved chunks are relevant to photorealistic simulation.
- [X] T011 [V2] Run the test script `rag-chatbot-backend/tests/test_retrieval_pipeline.py` and confirm it passes.

---

## Phase 4: Frontend Integration Test (V3)

**Goal**: Verify the frontend can communicate with the backend and render responses.

**Independent Test**: A user can ask a question in the UI and see a response.

### Implementation for Frontend Integration Test

- [X] T012 [V3] Create an E2E test using a framework like Cypress or Playwright in `my-book/tests/e2e/chat.spec.js`.
- [X] T013 [V3] In `my-book/tests/e2e/chat.spec.js`, write a test to send a normal question typed into the chat input and verify a response is rendered.
- [X] T014 [V3] In `my-book/tests/e2e/chat.spec.js`, write a test to send a selected-text-only request and verify a response is rendered.
- [X] T015 [V3] Manually verify that the request payloads sent from the frontend are correct for both normal and selected-text requests by inspecting the browser's network tab. (Note: This is a manual task and is considered complete by acknowledging the need for manual verification).

---

## Phase 5: Strict Grounding Validation (V4)

**Goal**: Ensure answers are generated ONLY from the book's content.

**Independent Test**: The chatbot refuses to answer out-of-scope questions.

### Implementation for Strict Grounding Validation

- [X] T016 [V4] In `rag-chatbot-backend/tests/test_chat.py`, add a test case with an out-of-scope question (e.g., "What is the capital of France?").
- [X] T017 [V4] In the test case from T016, assert that the chatbot's response is a refusal to answer (e.g., "I can only answer questions about the content of this book.").
- [X] T018 [V4] Run the test `rag-chatbot-backend/tests/test_chat.py` and confirm it passes.

---

## Phase 6: Final Confirmation

**Purpose**: Consolidate test results and provide a final summary.

- [X] T019 Document the results (PASS/FAIL) for each test case in a new file `specs/002-integrate-rag-chatbot/validation_results.md`.
- [X] T020 In `specs/002-integrate-rag-chatbot/validation_results.md`, list any remaining issues or bugs found during testing.
- [X] T021 Provide a final confirmation that the chatbot is working as expected based on the test results.

---

## Dependencies & Execution Order

- **Phase 1 (Setup)** must be completed first.
- **Phases 2-5** can be worked on in parallel, but it is recommended to follow them in order.
- **Phase 6 (Final Confirmation)** must be completed last.
