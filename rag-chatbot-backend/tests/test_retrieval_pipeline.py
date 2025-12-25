import pytest
from unittest.mock import patch, MagicMock
from app.services.retrieval import retrieve_chunks

@patch('app.services.retrieval.search_vectors')
@patch('app.services.retrieval.generate_embeddings')
def test_retrieve_chunks_ros2(mock_generate_embeddings, mock_search_vectors):
    # Arrange
    mock_generate_embeddings.return_value = [[0.1] * 768]
    mock_search_vectors.return_value = [
        MagicMock(payload={'content': 'ROS 2 is a set of software libraries and tools.', 'source_url': 'http://example.com/ros2', 'page_title': 'ROS 2'}),
        MagicMock(payload={'content': 'It is used for building robot applications.', 'source_url': 'http://example.com/ros2', 'page_title': 'ROS 2'})
    ]
    query = "What is ROS 2?"

    # Act
    retrieved = retrieve_chunks(query)

    # Assert
    mock_generate_embeddings.assert_called_once_with([query])
    mock_search_vectors.assert_called_once_with([0.1] * 768, limit=5)
    assert len(retrieved) == 2
    assert retrieved[0]['content'] == 'ROS 2 is a set of software libraries and tools.'
    assert retrieved[0]['source_url'] == 'http://example.com/ros2'
    assert retrieved[1]['content'] == 'It is used for building robot applications.'
    assert retrieved[1]['source_url'] == 'http://example.com/ros2'

@patch('app.services.retrieval.search_vectors')
@patch('app.services.retrieval.generate_embeddings')
def test_retrieve_chunks_photorealistic_simulation(mock_generate_embeddings, mock_search_vectors):
    # Arrange
    mock_generate_embeddings.return_value = [[0.2] * 768]
    mock_search_vectors.return_value = [
        MagicMock(payload={'content': 'Photorealistic simulation aims to create images that are indistinguishable from reality.', 'source_url': 'http://example.com/simulation', 'page_title': 'Simulation'}),
        MagicMock(payload={'content': 'It is often used in movies and video games.', 'source_url': 'http://example.com/simulation', 'page_title': 'Simulation'})
    ]
    query = "Explain photorealistic simulation"

    # Act
    retrieved = retrieve_chunks(query)

    # Assert
    mock_generate_embeddings.assert_called_once_with([query])
    mock_search_vectors.assert_called_once_with([0.2] * 768, limit=5)
    assert len(retrieved) == 2
    assert retrieved[0]['content'] == 'Photorealistic simulation aims to create images that are indistinguishable from reality.'
    assert retrieved[0]['source_url'] == 'http://example.com/simulation'
    assert retrieved[1]['content'] == 'It is often used in movies and video games.'
    assert retrieved[1]['source_url'] == 'http://example.com/simulation'