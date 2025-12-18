import requests
from xml.etree import ElementTree as ET
from unstructured.partition.html import partition_html
from unstructured.chunking.title import chunk_by_title

def get_sitemap_urls(sitemap_url: str) -> list[str]:
    response = requests.get(sitemap_url)
    response.raise_for_status()
    
    root = ET.fromstring(response.content)
    urls = []
    
    namespace = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    
    for url_element in root.findall('sitemap:url', namespace):
        loc_element = url_element.find('sitemap:loc', namespace)
        if loc_element is not None:
            urls.append(loc_element.text)
            
    return urls

def fetch_and_chunk_url(url: str):
    response = requests.get(url)
    response.raise_for_status()
    
    elements = partition_html(text=response.text)
    chunks = chunk_by_title(elements)
    
    # Extract text content from each chunk element
    text_chunks = []
    for chunk in chunks:
        if hasattr(chunk, 'text'):
            text_chunks.append(chunk.text)
    return text_chunks

if __name__ == "__main__":
    docusaurus_sitemap_url = "http://localhost:3000/sitemap.xml" 
    
    try:
        page_urls = get_sitemap_urls(docusaurus_sitemap_url)
        print(f"Found {len(page_urls)} URLs:")
        for url in page_urls:
            print(f"Processing URL: {url}")
            content_chunks = fetch_and_chunk_url(url)
            for i, chunk in enumerate(content_chunks):
                print(f"  Chunk {i+1}: {chunk[:200]}...") # Print first 200 chars
            if not content_chunks:
                print("  No chunks found for this URL.")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
