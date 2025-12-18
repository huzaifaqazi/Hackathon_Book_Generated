from ..services.vector_store import search_vectors
from ..services.embeddings import generate_embeddings
from qdrant_client import models

def retrieve_chunks(query: str, limit: int = 5) -> list[dict]:
    query_embedding = generate_embeddings([query])[0]
    
    search_results = search_vectors(query_embedding, limit=limit)
    
    # Extract relevant information from search results
    retrieved_info = []
    for hit in search_results:
        retrieved_info.append({
            "content": hit.payload.get("content"),
            "source_url": hit.payload.get("source_url"),
            "page_title": hit.payload.get("page_title"),
            "score": hit.score
        })
    return retrieved_info

if __name__ == "__main__":
    # This example requires QDRANT_HOST and QDRANT_API_KEY to be set,
    # and for the Qdrant collection to have some data.
    # from ..services.ingestion import perform_ingestion
    # import asyncio
    # asyncio.run(perform_ingestion("http://localhost:3000/sitemap.xml")) # Run this once to populate Qdrant

    test_query = "What are the hardware requirements?"
    results = retrieve_chunks(test_query)
    print(f"Retrieved {len(results)} chunks for query: '{test_query}'")
    for res in results:
        print(f"  - Score: {res['score']}, URL: {res['source_url']}, Content: {res['content'][:100]}...")
