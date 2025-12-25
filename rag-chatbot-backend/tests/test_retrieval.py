import pytest
from unittest.mock import patch, MagicMock
from rag-chatbot-backend.app.services.retrieval import retrieve_chunks

@patch('rag-chatbot-backend.app.services.retrieval.generate_embeddings')
@patch('rag-chatbot-backend.app.services.retrieval.search_vectors')
def test_retrieve_chunks(mock_search_vectors, mock_generate_embeddings):
    # Mock embedding generation
    mock_generate_embeddings.return_value = [[0.1] * 384]

    # Mock Qdrant search results
    mock_hit1 = MagicMock()
    mock_hit1.payload = {"content": "Chunk A", "source_url": "url_a", "page_title": "Page A"}
    mock_hit1.score = 0.9
    mock_hit2 = MagicMock()
    mock_hit2.payload = {"content": "Chunk B", "source_url": "url_b", "page_title": "Page B"}
    mock_hit2.score = 0.8
    mock_search_vectors.return_value = [mock_hit1, mock_hit2]

    query = "test query"
    results = retrieve_chunks(query)

    assert len(results) == 2
    assert results[0]["content"] == "Chunk A"
    assert results[0]["source_url"] == "url_a"
    assert results[0]["score"] == 0.9
    assert results[1]["content"] == "Chunk B"
