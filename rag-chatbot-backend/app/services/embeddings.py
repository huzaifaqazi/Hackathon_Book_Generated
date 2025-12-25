import os
import time
import cohere
from dotenv import load_dotenv
from loguru import logger
import tenacity

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY environment variable not set.")

co = cohere.Client(COHERE_API_KEY)

COHERE_EMBED_MODEL = "embed-english-light-v3.0"

@tenacity.retry(
    wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
    stop=tenacity.stop_after_attempt(5),
    retry=tenacity.retry_if_exception_type(Exception),
    reraise=True,
)
def _generate_embeddings_with_retry(texts: list[str]) -> list[list[float]]:
    """
    Helper function for generating embeddings with retry logic using Cohere API.
    """
    logger.info(f"Generating embeddings for a batch of {len(texts)} texts...")
    response = co.embed(texts=texts, model=COHERE_EMBED_MODEL, input_type="search_document")
    return response.embeddings

def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Generates embeddings for a list of texts using the Cohere API with batching.
    """
    logger.info(f"Generating embeddings for {len(texts)} texts with Cohere...")
    start_time = time.time()
    all_embeddings = []
    
    # Cohere has a limit of 96 texts per request for the embed API.
    batch_size = 96
    
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i + batch_size]
        try:
            embeddings_batch = _generate_embeddings_with_retry(batch_texts)
            all_embeddings.extend(embeddings_batch)
        except Exception as e:
            logger.error(f"Failed to generate embeddings with Cohere after multiple retries: {e}")
            raise
    
    end_time = time.time()
    logger.info(f"Generated {len(all_embeddings)} embeddings in {end_time - start_time:.2f} seconds.")
    return all_embeddings

if __name__ == "__main__":
    test_texts = [
        "What is ROS2?",
        "How do I set up a Python environment?"
    ]
    embeddings = generate_embeddings(test_texts)
    print(f"Generated {len(embeddings)} embeddings. First embedding shape: {len(embeddings[0])}")
