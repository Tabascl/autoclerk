import requests
from bs4 import BeautifulSoup
import re

discord_hook_url = ''

data = {
    "content": "lul http://google.de/"
}

# requests.post(discord_hook_url, data=data)

scrape_url = 'https://www.alternate.de/Grafikkarten/RTX-3080'

page = requests.get(scrape_url)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find_all('div', class_='listRow')

for item in results:
    name_span = item.find('span', class_='name')
    stock_span = item.find('span', class_=re.compile('stockStatus*'))
    price_span = item.find('span', class_=re.compile('price*'))
    print("Price: {}, Name: {},\tAvailable: {}".format(price_span.get_text().strip(), name_span.get_text().strip(), stock_span.get_text().strip()))
