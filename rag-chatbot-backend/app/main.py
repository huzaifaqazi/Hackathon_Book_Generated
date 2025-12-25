from fastapi import FastAPI, Request, status, BackgroundTasks, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import uuid
from uuid import UUID
import nltk
from loguru import logger
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.services.retrieval import retrieve_chunks
from app.services.agent import get_answer_from_agent
from app.services.llm import get_llm_response, OPENROUTER_MODEL
from app.core.db import get_db, SessionLocal, ChatSession, QueryLog, create_db_tables
from sqlalchemy.orm import Session


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Using OpenRouter model: {OPENROUTER_MODEL}")
    create_db_tables()

    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt")
    try:
        nltk.data.find("corpora/wordnet")
    except LookupError:
        nltk.download("wordnet")

    print("Startup tasks completed.")
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    query: str
    session_id: Optional[UUID] = None
    selected_text: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    sources: List[dict]

@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_with_rag_direct(request: ChatRequest, db: Session = Depends(get_db)):
    session_id = request.session_id or uuid.uuid4()

    retrieved_context = []
    if not request.selected_text:
        try:
            retrieved_context = retrieve_chunks(request.query)
        except Exception as e:
            logger.exception(f"Error retrieving chunks: {e}")

    system_prompt = "You are a helpful assistant that answers questions based only on provided context."
    context_text = "\n\n".join([c["content"] for c in retrieved_context]) if retrieved_context else ""
    full_prompt = f"{context_text}\n\nQuestion: {request.query}" if context_text else request.query

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": full_prompt}
    ]

    try:
        answer = get_llm_response(messages)
    except Exception as e:
        logger.exception(f"Error calling LLM: {e}")
        answer = "Sorry, the language model is currently unavailable."

    sources = [{"content": c["content"], "source_url": c["source_url"]} for c in retrieved_context] if retrieved_context else []

    try:
        query_log = QueryLog(
            session_id=session_id,
            query=request.query,
            retrieved_chunks=[{"content": c["content"], "source_url": c["source_url"], "score": c.get("score", 0)} for c in retrieved_context],
            response=answer
        )
        db.add(query_log)
        db.commit()
    except Exception as e:
        logger.exception(f"Error logging query: {e}")

    return ChatResponse(response=answer, session_id=str(session_id), sources=sources)


@app.get("/")
async def read_root():
    return {"message": "RAG Chatbot Backend is running!"}


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception for request: {request.url}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": f"An unexpected error occurred: {str(exc)}"},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
