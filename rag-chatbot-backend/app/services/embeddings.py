import os
import cohere
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")

if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY environment variable not set.")

co = cohere.Client(COHERE_API_KEY)

def generate_embeddings(texts: list[str]) -> list[list[float]]:
    response = co.embed(
        texts=texts,
        model="embed-english-light-v3.0", # Using a common embedding model
        input_type="search_document"
    )
    return response.embeddings

if __name__ == "__main__":
    test_texts = [
        "What is ROS2?",
        "How do I set up a Python environment?"
    ]
    embeddings = generate_embeddings(test_texts)
    print(f"Generated {len(embeddings)} embeddings. First embedding shape: {len(embeddings[0])}")
