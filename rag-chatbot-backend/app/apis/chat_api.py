from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import uuid

from ..services.retrieval import retrieve_chunks
from ..services.agent import get_answer_from_agent
from ..core.db import get_db, SessionLocal, ChatSession, QueryLog
from sqlalchemy.orm import Session

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    selected_text: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    sources: List[dict]

@router.post("/chat", response_model=ChatResponse)
async def chat_with_rag(request: ChatRequest, db: Session = Depends(get_db)):
    session_id = request.session_id
    if not session_id:
        session_id = str(uuid.uuid4())
        new_session = ChatSession(session_id=session_id)
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
    else:
        current_session = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
        if not current_session:
            raise HTTPException(status_code=404, detail="Session not found")
    
    retrieved_context = []
    if not request.selected_text:
        retrieved_context = retrieve_chunks(request.query)

    answer, sources = get_answer_from_agent(request.query, retrieved_context, request.selected_text)

    # Log the query and response
    query_log = QueryLog(
        session_id=session_id,
        query=request.query,
        retrieved_chunks=[{"content": c["content"], "source_url": c["source_url"], "score": c["score"]} for c in retrieved_context],
        response=answer
    )
    db.add(query_log)
    db.commit()

    return ChatResponse(response=answer, session_id=session_id, sources=sources)
