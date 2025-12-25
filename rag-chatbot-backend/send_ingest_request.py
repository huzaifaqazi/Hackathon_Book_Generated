import requests
import os
import json

backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
chat_endpoint = f"{backend_url}/api/v1/chat"

query = "what is physical Ai?"
# For a new session, don't provide session_id
payload = {"query": query} 

print(f"Attempting to send POST request to: {chat_endpoint} with JSON payload: {json.dumps(payload)}")

try:
    response = requests.post(chat_endpoint, json=payload)
    response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
    print("Chat request successful!")
    print("Response Status Code:", response.status_code)
    print("Response Body:", response.json())
except requests.exceptions.ConnectionError as e:
    print(f"Connection Error: Could not connect to the backend server. Is it running? {e}")
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: An HTTP error occurred: {e}")
    print("Response Status Code:", e.response.status_code)
    print("Response Body:", e.response.text)
except requests.exceptions.Timeout as e:
    print(f"Timeout Error: The request timed out: {e}")
except requests.exceptions.RequestException as e:
    print(f"An unexpected error occurred: {e}")
except Exception as e:
    print(f"A general error occurred: {e}")