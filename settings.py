import os

ITEM_NAME = os.environ['ITEM_NAME']
GOOD_THRESHOLD = int(os.environ['THRESHOLD'])
QUERY_FREQ_MINUTES = int(os.environ['FREQ_MIN'])

WEBSITE = 'avito.ru'
CACHE_SIZE = 100 # hours