
import asyncio
from app.services.ingestion import perform_ingestion
import os

async def main():
    sitemap_path = os.getenv("DOCUSAURUS_SITEMAP_PATH", "D:/Hackathon/ai-native-book/my-book/Hackathon_Book_Generated/sitemap.xml")
    await perform_ingestion(sitemap_path)

if __name__ == "__main__":
    asyncio.run(main())
