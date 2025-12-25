import requests
import json

url = "http://127.0.0.1:8000/api/v1/chat"
payload = {"query": "What is the Module 2?"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(payload), headers=headers)

print(response.json())