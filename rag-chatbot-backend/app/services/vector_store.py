import os
from qdrant_client import QdrantClient, models
from dotenv import load_dotenv

from loguru import logger

load_dotenv()

QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_HOST = os.getenv("QDRANT_HOST") # e.g., 'https://[cluster-url].qdrant.tech'

if not QDRANT_API_KEY or not QDRANT_HOST:
    raise ValueError("QDRANT_API_KEY and QDRANT_HOST environment variables not set.")

COLLECTION_NAME = "book_chunks"
VECTOR_SIZE = 384 # Cohere's embed-english-light-v3.0 typically produces 384-dim vectors

_qdrant_client = None

def get_qdrant_client():
    global _qdrant_client
    if _qdrant_client is None:
        logger.info("Initializing QdrantClient...")
        _qdrant_client = QdrantClient(
            url=QDRANT_HOST, 
            api_key=QDRANT_API_KEY,
        )
        logger.info("QdrantClient initialized.")
    return _qdrant_client

def create_collection_if_not_exists():
    client = get_qdrant_client()
    logger.info(f"Checking if collection '{COLLECTION_NAME}' exists...")
    if not client.collection_exists(collection_name=COLLECTION_NAME):
        logger.info(f"Collection '{COLLECTION_NAME}' does not exist. Creating...")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(size=VECTOR_SIZE, distance=models.Distance.COSINE),
        )
        logger.info(f"Collection '{COLLECTION_NAME}' created with {VECTOR_SIZE} dimensions and Cosine distance.")
    else:
        logger.info(f"Collection '{COLLECTION_NAME}' already exists.")

def upload_vectors(points: list[models.PointStruct]):
    client = get_qdrant_client()
    operation_info = client.upsert(
        collection_name=COLLECTION_NAME,
        wait=True,
        points=points,
    )
    print(f"Upsert operation info: {operation_info}")

def search_vectors(query_vector: list[float], limit: int = 5) -> list[models.ScoredPoint]:
    client = get_qdrant_client()
    search_result = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=limit,
    )
    return search_result

if __name__ == "__main__":
    # Example usage:
    create_collection_if_not_exists()

    # You would typically generate embeddings for real data here
    # from embeddings import generate_embeddings
    # sample_texts = ["This is a test document.", "Another document for testing."]
    # sample_embeddings = generate_embeddings(sample_texts)

    # For demonstration, creating dummy points
    dummy_points = [
        models.PointStruct(
            id=1,
            vector=[0.1] * VECTOR_SIZE, # Dummy vector
            payload={"content": "This is a test chunk from chapter 1.", "url": "http://example.com/ch1"},
        ),
        models.PointStruct(
            id=2,
            vector=[0.2] * VECTOR_SIZE, # Dummy vector
            payload={"content": "Another test chunk from chapter 2.", "url": "http://example.com/ch2"},
        ),
    ]
    # upload_vectors(dummy_points)

    # Dummy search
    # query_vector = [0.15] * VECTOR_SIZE
    # search_results = search_vectors(query_vector)
    # print("Search results:")
    # for result in search_results:
    #     print(f"  Score: {result.score}, Content: {result.payload['content']}")
