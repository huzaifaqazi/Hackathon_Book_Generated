import pytest
from unittest.mock import patch
from app.services.agent import get_answer_from_agent

@patch('app.services.agent.get_llm_response')
def test_get_answer_from_agent_with_context(mock_get_llm_response):
    # Arrange
    mock_get_llm_response.return_value = "This is a test response."
    query = "What is a test?"
    retrieved_context = [
        {
            "content": "A test is a procedure intended to establish the quality, performance, or reliability of something.",
            "source_url": "http://example.com/test",
            "page_title": "Test"
        }
    ]
    selected_text = None

    # Act
    answer, sources = get_answer_from_agent(query, retrieved_context, selected_text)

    # Assert
    assert answer == "This is a test response."
    assert sources is not None
    assert len(sources) == 1
    assert sources[0]["url"] == "http://example.com/test"

@patch('app.services.agent.get_llm_response')
def test_get_answer_from_agent_with_selected_text(mock_get_llm_response):
    # Arrange
    mock_get_llm_response.return_value = "This is a test response for selected text."
    query = "What is this about?"
    retrieved_context = []
    selected_text = "This is a snippet of text about a specific topic."

    # Act
    answer, sources = get_answer_from_agent(query, retrieved_context, selected_text)

    # Assert
    assert answer == "This is a test response for selected text."
    assert sources is not None
    assert len(sources) == 0

@patch('app.services.agent.get_llm_response')
def test_get_answer_from_agent_no_context(mock_get_llm_response):
    # Arrange
    mock_get_llm_response.return_value = "This is a test response with no context."
    query = "What is a test?"
    retrieved_context = []
    selected_text = None

    # Act
    answer, sources = get_answer_from_agent(query, retrieved_context, selected_text)

    # Assert
    assert answer == "This is a test response with no context."
    assert sources is not None
    assert len(sources) == 0
