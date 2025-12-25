import requests
from xml.etree import ElementTree as ET
from unstructured.partition.html import partition_html
from unstructured.chunking.title import chunk_by_title
from loguru import logger
import os

from app.services.embeddings import generate_embeddings
from app.services.vector_store import recreate_collection, upload_vectors, COLLECTION_NAME, COHERE_EMBED_MODEL_NAME
from qdrant_client import models

def get_sitemap_urls(sitemap_path: str) -> list[str]:
    try:
        # Check if sitemap_path is a local file or a URL
        if sitemap_path.startswith("http://") or sitemap_path.startswith("https://"):
            logger.info(f"Fetching sitemap from URL: {sitemap_path}")
            response = requests.get(sitemap_path, timeout=10)
            response.raise_for_status()
            sitemap_content = response.text
        else:
            logger.info(f"Reading sitemap from local file: {sitemap_path}")
            with open(sitemap_path, 'r', encoding='utf-8') as f:
                sitemap_content = f.read()

        root = ET.fromstring(sitemap_content)
        urls = []
        
        namespace = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        for url_element in root.findall('sitemap:url', namespace):
            loc_element = url_element.find('sitemap:loc', namespace)
            if loc_element is not None:
                urls.append(loc_element.text)
                
        logger.info(f"Successfully retrieved {len(urls)} URLs from sitemap: {sitemap_path}")
        return urls
    except FileNotFoundError:
        logger.error(f"Sitemap file not found at {sitemap_path}. Please ensure the path is correct.")
        return []
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching sitemap from URL {sitemap_path}: {e}")
        return []
    except ET.ParseError as e:
        logger.error(f"Error parsing sitemap XML from {sitemap_path}: {e}")
        return []

def fetch_and_chunk_url(url: str):
    try:
        response = requests.get(url, timeout=10) # Added timeout
        response.raise_for_status()
        
        elements = partition_html(text=response.text)
        chunks = chunk_by_title(elements)
        
        text_chunks = []
        for chunk in chunks:
            if hasattr(chunk, 'text'):
                chunk_dict = chunk.to_dict() # Convert to dictionary to safely access attributes
                chunk_content = chunk.text
                chunk_element_type = chunk_dict.get("type")
                
                logger.debug(f"  Chunk Type: {chunk_element_type}, Content Snippet: {chunk_content[:100]}...")

                text_chunks.append({
                    "content": chunk_content,
                    "source_url": url,
                    "element_type": chunk_element_type
                })
        logger.info(f"Successfully fetched and chunked {len(text_chunks)} from URL: {url}")
        return text_chunks
    except requests.exceptions.Timeout:
        logger.error(f"Timeout while fetching content from {url}.")
        return []
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching content from {url}: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error during chunking for {url}: {e}")
        return []

async def perform_ingestion(sitemap_path: str):
    logger.info("Starting ingestion process...")
    recreate_collection() # Start with a fresh collection

    page_urls = get_sitemap_urls(sitemap_path)
    if not page_urls:
        logger.warning("No URLs found in sitemap. Ingestion aborted.")
        return

    all_points = []
    point_id_counter = 0

    for url in page_urls:
        logger.info(f"Processing URL: {url}")
        content_chunks = fetch_and_chunk_url(url)
        
        if content_chunks:
            # Extract text for embedding
            texts_to_embed = [chunk["content"] for chunk in content_chunks]
            embeddings = generate_embeddings(texts_to_embed)

            for i, chunk in enumerate(content_chunks):
                if i < len(embeddings):
                    point_id_counter += 1
                    all_points.append(
                        models.PointStruct(
                            id=point_id_counter,
                            vector={COHERE_EMBED_MODEL_NAME: embeddings[i]},
                            payload={
                                "content": chunk["content"],
                                "source_url": chunk["source_url"],
                                "element_type": chunk["element_type"]
                            },
                        )
                    )
                else:
                    logger.warning(f"Embedding missing for chunk {i} from {url}. Skipping.")
        else:
            logger.info(f"No content chunks found for URL: {url}")

    if all_points:
        logger.info(f"Uploading {len(all_points)} points to Qdrant collection '{COLLECTION_NAME}'...")
        upload_vectors(all_points)
        logger.info("Ingestion process completed successfully.")
    else:
        logger.warning("No points to upload. Ingestion finished with no data.")

if __name__ == "__main__":
    # This block is for testing purposes only
    # In real usage, perform_ingestion is called from run_ingestion.py
    # Example usage (replace with your Docusaurus sitemap URL or local path)
    docusaurus_sitemap_path = os.getenv("DOCUSAURUS_SITEMAP_PATH", "D:/Hackathon/ai-native-book/my-book/Hackathon_Book_Generated/sitemap.xml")
    import asyncio
    asyncio.run(perform_ingestion(docusaurus_sitemap_path))
