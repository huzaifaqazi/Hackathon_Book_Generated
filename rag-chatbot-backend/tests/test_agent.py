import pytest
from unittest.mock import patch, MagicMock
from rag-chatbot-backend.app.services.agent import construct_agent_prompt, get_answer_from_agent

@pytest.fixture
def sample_retrieved_context():
    return [
        {"content": "ROS 2 is a robotics middleware.", "source_url": "url1", "page_title": "ROS2 Intro"},
        {"content": "Python is used for ROS 2 programming.", "source_url": "url2", "page_title": "Python for ROS2"},
    ]

@patch('rag-chatbot-backend.app.services.agent.get_llm_response')
def test_get_answer_from_agent_full_book(mock_get_llm_response, sample_retrieved_context):
    mock_get_llm_response.return_value = "The answer about ROS 2."
    
    query = "What is ROS2?"
    answer, sources = get_answer_from_agent(query, sample_retrieved_context)

    assert answer == "The answer about ROS 2."
    assert len(sources) == 2
    assert {"url": "url1", "title": "ROS2 Intro"} in sources
    mock_get_llm_response.assert_called_once()
    args, kwargs = mock_get_llm_response.call_args
    messages = args[0]
    assert messages[0]["role"] == "system"
    assert "ONLY on the provided context" in messages[0]["content"]
    assert messages[1]["role"] == "user"
    assert "What is ROS2?" in messages[1]["content"]
    assert "ROS 2 is a robotics middleware." in messages[1]["content"]

@patch('rag-chatbot-backend.app.services.agent.get_llm_response')
def test_get_answer_from_agent_selected_text(mock_get_llm_response):
    mock_get_llm_response.return_value = "Selected text answer."
    
    query = "Explain this."
    selected_text = "This is important information."
    answer, sources = get_answer_from_agent(query, [], selected_text) # No retrieved context

    assert answer == "Selected text answer."
    assert sources == [] # No sources if only selected_text is used
    mock_get_llm_response.assert_called_once()
    args, kwargs = mock_get_llm_response.call_args
    messages = args[0]
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"
    assert "Based ONLY on this selected text" in messages[1]["content"]
    assert selected_text in messages[1]["content"]
