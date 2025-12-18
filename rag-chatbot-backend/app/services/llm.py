import os
from openai import OpenAI # OpenRouter uses OpenAI's client
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo") # Default model

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY environment variable not set.")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

def get_llm_response(messages: list[dict]) -> str:
    response = client.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=messages,
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    test_messages = [
        {"role": "user", "content": "What is the capital of France?"}
    ]
    try:
        response_content = get_llm_response(test_messages)
        print(f"LLM Response: {response_content}")
    except Exception as e:
        print(f"Error getting LLM response: {e}")
