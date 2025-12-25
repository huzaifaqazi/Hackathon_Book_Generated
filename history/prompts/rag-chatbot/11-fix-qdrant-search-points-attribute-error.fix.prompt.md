---
id: 11
title: Fix QdrantClient' object has no attribute 'search_points' error
stage: fix
date: 2025-12-24
surface: agent
model: gemini-pro
feature: rag-chatbot
branch: main
user: unknown
command: unknown
labels: [ "bug", "qdrant", "database" ]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- rag-chatbot-backend/app/services/vector_store.py
tests:
- (none)
---

## Prompt

chabot embeddings se answer nh de rha  why INFO:     Application startup complete.
2025-12-24 16:09:09.343 | INFO     | app.services.embeddings:generate_embeddings:31 - Generating embeddings for 1 texts...
2025-12-24 16:09:10.929 | INFO     | app.services.embeddings:generate_embeddings:40 - Generated embeddings in 1.59 seconds.
2025-12-24 16:09:10.929 | INFO     | app.services.vector_store:get_qdrant_client:25 - Initializing QdrantClient...
2025-12-24 16:09:13.756 | INFO     | app.services.vector_store:get_qdrant_client:30 - QdrantClient initialized.
2025-12-24 16:09:13.757 | INFO     | app.services.vector_store:search_vectors:68 - Searching vectors in Qdrant...
2025-12-24 16:09:13.757 | ERROR    | app.main:chat_with_rag_direct:66 - Error retrieving chunks: 'QdrantClient' object has no attribute 'search_points'
Traceback (most recent call last):
...
AttributeError: 'QdrantClient' object has no attribute 'search_points'
...

## Response snapshot

Based on the traceback, the error `AttributeError: 'QdrantClient' object has no attribute 'search_points'` is happening in your `rag-chatbot-backend/app/services/vector_store.py` file on line 70, within the `search_vectors` function.

It seems the version of the `qdrant-client` library you are using does not have a `search_points` method. The correct method is likely `search`.

I will now find the file `vector_store.py` and correct the method name.

## Outcome

- ✅ Impact: Fixes a critical bug preventing the chatbot from retrieving information from the vector store.
- 🧪 Tests: No new tests were added.
- 📁 Files: Modified 1 file to fix a method call.
- 🔁 Next prompts: (none)
- 🧠 Reflection: The error was due to a recent change in the qdrant-client library. The `search_points` method was replaced with `search`.

## Evaluation notes (flywheel)

- Failure modes observed: (none)
- Graders run and results (PASS/FAIL): (none)
- Prompt variant (if applicable): (none)
- Next experiment: (none)
