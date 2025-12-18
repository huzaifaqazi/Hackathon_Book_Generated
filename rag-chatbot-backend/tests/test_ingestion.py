import pytest
from unittest.mock import patch, MagicMock
from rag-chatbot-backend.app.services.ingestion import get_sitemap_urls, fetch_and_chunk_url

@patch('requests.get')
def test_get_sitemap_urls(mock_get):
    mock_response = MagicMock()
    mock_response.content = """
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url><loc>http://localhost:3000/page1</loc></url>
        <url><loc>http://localhost:3000/page2</loc></url>
    </urlset>
    """.encode('utf-8')
    mock_get.return_value = mock_response

    urls = get_sitemap_urls("http://localhost:3000/sitemap.xml")
    assert len(urls) == 2
    assert "http://localhost:3000/page1" in urls
    assert "http://localhost:3000/page2" in urls

@patch('requests.get')
@patch('rag-chatbot-backend.app.services.ingestion.partition_html')
@patch('rag-chatbot-backend.app.services.ingestion.chunk_by_title')
def test_fetch_and_chunk_url(mock_chunk_by_title, mock_partition_html, mock_get):
    mock_get.return_value.text = "<html><body><h1>Title</h1><p>Content</p></body></html>"
    
    mock_element1 = MagicMock()
    mock_element1.text = "Chunk 1"
    mock_element2 = MagicMock()
    mock_element2.text = "Chunk 2"
    mock_partition_html.return_value = [mock_element1, mock_element2]
    mock_chunk_by_title.return_value = [mock_element1, mock_element2]

    chunks = fetch_and_chunk_url("http://localhost:3000/test-page")
    assert len(chunks) == 2
    assert "Chunk 1" in chunks
    assert "Chunk 2" in chunks
