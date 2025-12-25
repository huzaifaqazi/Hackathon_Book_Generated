import pytest
import requests
import json
from unittest.mock import patch

# --- Test Data ---
BASE_URL = "http://127.0.0.1:8000/api/v1/chat"
HEADERS = {"Content-Type": "application/json"}

# --- Test Cases ---

@patch('app.main.get_answer_from_agent')
def test_chat_endpoint_in_scope(mock_get_answer_from_agent, requests_mock):
    """
    Tests the /api/v1/chat endpoint with an in-scope question.
    """
    # Arrange
    mock_get_answer_from_agent.return_value = ("A digital twin is a virtual model of a physical object.", [{"url": "http://example.com/dt", "title": "Digital Twin"}])
    requests_mock.post(BASE_URL, json={"response": "A digital twin is a virtual model of a physical object.", "sources": [{"url": "http://example.com/dt", "title": "Digital Twin"}]})

    payload = {"query": "What is a digital twin?"}

    # Act
    response = requests.post(BASE_URL, data=json.dumps(payload), headers=HEADERS)
    
    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert "A digital twin" in response_data['response']
    assert len(response_data['sources']) > 0

@patch('app.main.get_answer_from_agent')
def test_chat_endpoint_out_of_scope(mock_get_answer_from_agent, requests_mock):
    """
    Tests the /api/v1/chat endpoint with an out-of-scope question.
    """
    # Arrange
    mock_get_answer_from_agent.return_value = ("I can only answer questions about the content of this book.", [])
    requests_mock.post(BASE_URL, json={"response": "I can only answer questions about the content of this book.", "sources": []})

    payload = {"query": "What is the capital of France?"}

    # Act
    response = requests.post(BASE_URL, data=json.dumps(payload), headers=HEADERS)
    
    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert "I can only answer questions about the content of this book." in response_data['response']
    assert len(response_data['sources']) == 0

if __name__ == "__main__":
    pytest.main()