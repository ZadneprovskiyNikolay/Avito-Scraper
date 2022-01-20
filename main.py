# %%
from time import sleep

import requests
import urllib.request, urllib
from bs4 import BeautifulSoup
from requests import get

from item import Item
from headers import headers
from settings import ITEM_NAME, GOOD_THRESHOLD, QUERY_FREQ_MINUTES, WEBSITE, CACHE_SIZE


item_name_encoded = requests.utils.quote(ITEM_NAME)

recent_items = [] # Push queue during last 48 hours

while True:
    # %%
    items = []

    max_pages = 1
    for page_num in range(1, max_pages + 1):

        res = get(
            f'https://www.avito.ru/sankt-peterburg/telefony/mobilnye_telefony/apple-ASgBAgICAkS0wA3OqzmwwQ2I_Dc?cd=1&p={page_num}&q={item_name_encoded}&s=104',
            headers=headers
        )

        soup = BeautifulSoup(res.text)


        tree_items = soup.find_all('div', {'data-marker': 'item'})
        page_items = []

        for item in tree_items:
            title = item.find('h3', {'itemprop': 'name'}).text
            href = item.find('a', {'data-marker': 'item-title'})['href']
            href = f'{WEBSITE}{href}'
            date = item.find('div', {'data-marker': 'item-date'}).text        
            try:
                price = int(item.find('span', {'class': 'price-text-_YGDY'}).text[:-2].replace('\xa0', ''))
            except:
                continue
            
            page_items.append(Item(title=title, href=href, price=price, date_str=date))

        # Отсеиваю неподходящие
        page_items = list(filter(lambda item: (ITEM_NAME in item.title), page_items))

        if not page_items:
            print(f'page {page_num} aborting, response: {soup}')
            print()
            break

        items.extend(page_items)

        print(f'page {page_num}: {len(page_items)} items ({len(items)} total)')

    # %%
    items = list(set(items))
    print(f'total: {len(items)}')

    good = list(filter(lambda item: item.price <= GOOD_THRESHOLD, items))
    good = sorted(good, key=lambda x: (x.time, x.price))
    print(f'good: {len(good)}')

    print(len(good))    

    for item in good:

        # Check if item is already processed.
        if item not in recent_items:

            # Push item.
            urllib.request.urlopen(f'http://pushmebot.ru/send?key=c74bd2b6021a3f352e5c08762fb53b1e&message={item.href}')

            recent_items.append(item)
            if len(recent_items) > CACHE_SIZE:
                recent_items.pop(0)
    

        print(f'sleeping for {QUERY_FREQ_MINUTES} min...')
        sleep(QUERY_FREQ_MINUTES * 60)


# %%




