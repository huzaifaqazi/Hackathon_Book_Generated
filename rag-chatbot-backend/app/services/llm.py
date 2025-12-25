import os
import time
from dotenv import load_dotenv
from openai import OpenAI
from loguru import logger

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not set")

logger.info(f" OpenRouter model in use: {OPENROUTER_MODEL}")

_client = None

def get_openrouter_client():
    global _client
    if _client is None:
        logger.info("Initializing OpenRouter client...")
        _client = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
        )
    return _client


def get_llm_response(messages: list[dict]) -> str:
    client = get_openrouter_client()
    logger.info("Sending request to LLM...")
    start = time.time()

    try:
        completion = client.chat.completions.create(
            model=OPENROUTER_MODEL,
            messages=messages,
            max_tokens=512,        
            temperature=0.2,
        )

        logger.info(f"LLM responded in {time.time() - start:.2f}s")
        return completion.choices[0].message.content.strip()

    except Exception as e:
        logger.exception("Error while calling OpenRouter LLM")
        return "The language model is currently unavailable. Please try again later."


if __name__ == "__main__":
    test_messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "what is the The Digital Twin (Gazebo & Unity?"}
    ]
    print(get_llm_response(test_messages))
