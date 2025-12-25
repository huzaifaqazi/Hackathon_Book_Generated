import requests
import json

def test_chat_endpoint(query, selected_text=None):
    url = "http://127.0.0.1:8000/api/v1/chat"
    payload = {
        "query": query
    }
    if selected_text:
        payload["selected_text"] = selected_text

    headers = {
        'Content-Type': 'application/json'
    }

    print(f"--- Testing query: '{query}' ---")
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=5)
        response.raise_for_status()  # Raise an exception for bad status codes
        print("Status Code:", response.status_code)
        print("Response JSON:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        if e.response is not None:
            print("Response content:", e.response.text)
    print("--- End of test ---\
")

if __name__ == "__main__":
    queries = [
        "What is ROS 2?",
        "Explain photorealistic simulation",
        "What is the robotic nervous system?"
    ]
    for q in queries:
        test_chat_endpoint(q)

    # Test for grounding with a question not in the book
    test_chat_endpoint("What is the capital of France?")
