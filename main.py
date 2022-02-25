# %%

from time import sleep

import requests
import urllib.request, urllib
from bs4 import BeautifulSoup
from requests import get

from item import Item
from headers import headers
from settings import ITEM_NAME, GOOD_THRESHOLD, QUERY_FREQ_MINUTES, WEBSITE

def good_item(item):
    return ITEM_NAME.lower() in item.title.lower() and \
        item.price <= GOOD_THRESHOLD and \
            item.time * 60 <= QUERY_FREQ_MINUTES

item_name_encoded = requests.utils.quote(ITEM_NAME)

# %%
items = []

max_pages = 1
for page_num in range(1, max_pages + 1):

    res = get(
        f'https://www.avito.ru/sankt-peterburg?bt={page_num}&q={ITEM_NAME}',
        headers=headers
    )

    soup = BeautifulSoup(res.text)

    tree_items = soup.find_all('div', {'data-marker': 'item'})
    if not tree_items:
        print(f'page {page_num} aborting, response: {soup}')
        print()
        break

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
        print(page_items)

        # Отсеиваю неподходящие
        page_items = list(filter(good_item, page_items))

        items.extend(page_items)

        # print(f'page {page_num}: {len(page_items)} items ({len(items)} total)')

items = list(set(items))
items = sorted(items, key=lambda x: (x.time, x.price))

for item in items:
    # Push item.
    print(item.time * 60)
    urllib.request.urlopen(f'http://pushmebot.ru/send?key=c74bd2b6021a3f352e5c08762fb53b1e&message={item.href}')



