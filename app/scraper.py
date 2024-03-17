import asyncio
import time

import aiohttp
import requests
from bs4 import BeautifulSoup

from app.database import upload
from app.models import Item, Card
from app.misc import *


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()



async def scrape_card(url: str) -> list[Card]:
    try:
        cards = []
        async with aiohttp.ClientSession() as session:
            html = await fetch(session, url)
        soup = BeautifulSoup(html, features='html.parser')
        new_price = soup.find('span', {'data-qa': 'mfeCtaMain#offer0#finalPrice'}).text
        try:
            old_price = soup.find('span', {'data-qa': 'mfeCtaMain#offer0#originalPrice'}).text
        except:
            old_price = None
        description_element = soup.find('p', {'data-qa': 'mfe-game-overview#description'})
        for br in description_element.find_all("br"):
            br.replace_with("\n")

        description = description_element.text
        cards.append(Card(new_price, old_price, description, None))

        for edition in soup.find_all('article'):
            title = edition.findNext('h3', {'class': 'psw-t-title-s'}).text
            price_ = edition.findNext('span', {'class': 'psw-fill-x psw-l-line-left psw-m-b-2'}).text.split()[0].strip()
            print(url, price_)

            cards.append(Card(price_, price_, description, title))

        return cards
    except:
        return []


async def scrape_items():
    url = 'https://store.playstation.com/en-tr/pages/browse/'
    index = 0
    items: list = []
    full_time = time.time()

    while True:
        start = time.time()
        index += 1
        response = requests.get(url=f'{url}{index}')
        soup = BeautifulSoup(response.text, features='html.parser')
        elements = soup.find('ul', {'class': 'psw-grid-list psw-l-grid'}).find_all('li')
        if len(elements) == 0:
            break
        scrape_tasks = []
        flag = True
        for element in elements:
            try:
                href = 'https://store.playstation.com' + element.find('a').get('href')
            except:
                flag = False
                break
            try:
                task = scrape_card(href)
            except Exception as e:
                print('task error', e)
                continue
            scrape_tasks.append(task)
        if not flag:
            break
        results = await asyncio.gather(*scrape_tasks)

        for cards, element in zip(results, elements):
            to_upload = []
            try:
                for card in cards:
                    new_price, old_price = prepare_price(card.price), prepare_price(card.old_price)
                    old_price = new_price if old_price is None else old_price

                    old_price *= 4.1
                    new_price *= 4.1

                    href = 'https://store.playstation.com' + element.find('a').get('href')
                    title = element.find('section').text if card.title is None else card.title
                    img = element.find_all('img')[1].get('src')
                    if title in items:
                        continue

                    item = Item(
                        link=href,
                        title=title,
                        price=new_price,
                        old_price=old_price,
                        img=img,
                        description=translate(card.description)
                    )
                    to_upload.append(item)
                    items.append(item.title)
            except Exception as e:
                print(e)
            try:
                upload(to_upload)
            except:
                pass
        print(
            f'Items: {len(items)}. Iteration time: {round(time.time() - start, 2)}. Full time: {round(time.time() - full_time, 2)}.')

    return items
