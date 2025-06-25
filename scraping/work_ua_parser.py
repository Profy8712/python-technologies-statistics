import requests
from bs4 import BeautifulSoup
from config.config import SEARCH_URL, MAX_PAGES
import os
import json

def fetch_vacancies():
    all_vacancies = []

    for page in range(1, MAX_PAGES + 1):
        url = f"{SEARCH_URL}{page}"
        response = requests.get(url)
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div', class_='card')

        for card in cards:
            title_tag = card.find('h2')
            link_tag = title_tag.find('a') if title_tag else None
            description_tag = card.find('p')

            vacancy = {
                'title': title_tag.text.strip() if title_tag else '',
                'link': f"https://www.work.ua{link_tag['href']}" if link_tag else '',
                'description': description_tag.text.strip() if description_tag else ''
            }

            all_vacancies.append(vacancy)

    os.makedirs('data/raw', exist_ok=True)
    with open('data/raw/work_ua_vacancies.json', 'w', encoding='utf-8') as f:
        json.dump(all_vacancies, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(all_vacancies)} vacancies to data/raw/work_ua_vacancies.json")
