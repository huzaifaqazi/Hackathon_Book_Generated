from fastapi import APIRouter, HTTPException, BackgroundTasks
import requests
from ..services.ingestion import get_sitemap_urls, fetch_and_chunk_url
from ..services.embeddings import generate_embeddings
from ..services.vector_store import upload_vectors, create_collection_if_not_exists, COLLECTION_NAME
from qdrant_client import models
import uuid

router = APIRouter()

async def perform_ingestion(sitemap_url: str):
    try:
        create_collection_if_not_exists()
        urls = get_sitemap_urls(sitemap_url)
        
        for url in urls:
            try:
                chunks = fetch_and_chunk_url(url)
                if chunks:
                    embeddings = generate_embeddings(chunks)
                    
                    points = []
                    for i, chunk_text in enumerate(chunks):
                        point_id = uuid.uuid4().int
                        point = models.PointStruct(
                            id=point_id,
                            vector=embeddings[i],
                            payload={"content": chunk_text, "source_url": url, "page_title": url.split('/')[-1]},
                        )
                        points.append(point)
                    
                    if points:
                        upload_vectors(points)
                        print(f"Uploaded {len(points)} points for URL: {url}")
                else:
                    print(f"No chunks found for URL: {url}")
            except requests.exceptions.RequestException as e:
                print(f"Error fetching/chunking URL {url}: {e}")
            except Exception as e:
                print(f"An unexpected error occurred for URL {url}: {e}")
        
        print("Ingestion process completed.")

    except Exception as e:
        print(f"Global ingestion error: {e}")

@router.post("/ingest")
async def ingest_content(background_tasks: BackgroundTasks, sitemap_url: str = "http://localhost:3000/sitemap.xml"):
    """
    Triggers the content ingestion process for the Docusaurus book.
    Fetches sitemap, chunks content, generates embeddings, and uploads to Qdrant.
    """
    background_tasks.add_task(perform_ingestion, sitemap_url)
    return {"message": "Ingestion process started in the background."}
