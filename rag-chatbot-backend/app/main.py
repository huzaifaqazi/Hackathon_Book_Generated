from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
from .apis.ingestion_api import router as ingestion_router
from .apis.chat_api import router as chat_router
from fastapi.middleware.cors import CORSMiddleware
from .core.db import create_db_tables
import logging

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingestion_router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    create_db_tables()
    logger.info("Database tables checked/created on startup.")

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception for request: {request.url}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": f"An unexpected error occurred: {str(exc)}"},
    )

@app.get("/")
async def read_root():
    logger.info("Root endpoint accessed.")
    return {"message": "RAG Chatbot Backend is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
