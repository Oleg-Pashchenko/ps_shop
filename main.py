import asyncio

from app.scraper import scrape_items

if __name__ == '__main__':
    asyncio.run(scrape_items())
