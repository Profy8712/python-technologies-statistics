import asyncio
import aiohttp
import aiofiles
from bs4 import BeautifulSoup
from config.config import SEARCH_URL, MAX_PAGES
import os
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; AsyncScraper/1.0)"
}

async def fetch_page(session, page_number):
    url = f"{SEARCH_URL}{page_number}"
    async with session.get(url, headers=HEADERS) as response:
        if response.status != 200:
            print(f"Failed to fetch page {page_number}")
            return ""
        return await response.text()

def parse_vacancies_from_html(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    cards = soup.find_all('div', class_='card')

    vacancies = []
    for card in cards:
        title_tag = card.find('h2')
        link_tag = title_tag.find('a') if title_tag else None
        description_tag = card.find('p')

        vacancy = {
            'title': title_tag.text.strip() if title_tag else '',
            'link': f"https://www.work.ua{link_tag['href']}" if link_tag else '',
            'description': description_tag.text.strip() if description_tag else ''
        }

        vacancies.append(vacancy)

    return vacancies

async def scrape_all_pages():
    all_vacancies = []

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_page(session, page) for page in range(1, MAX_PAGES + 1)]
        pages_html = await asyncio.gather(*tasks)

        for html in pages_html:
            if html:
                page_vacancies = parse_vacancies_from_html(html)
                all_vacancies.extend(page_vacancies)

    os.makedirs('data/raw', exist_ok=True)
    async with aiofiles.open('data/raw/work_ua_vacancies_async.json', 'w', encoding='utf-8') as f:
        await f.write(json.dumps(all_vacancies, ensure_ascii=False, indent=2))

    print(f"Async scraper saved {len(all_vacancies)} vacancies to data/raw/work_ua_vacancies_async.json")

def run_async_scraper():
    asyncio.run(scrape_all_pages())
