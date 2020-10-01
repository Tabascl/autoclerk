import requests
from bs4 import BeautifulSoup
import re

scrape_url = 'https://www.alternate.de/Grafikkarten/RTX-3080'
scrape2 = 'https://www.caseking.de/pc-komponenten/grafikkarten/nvidia/geforce-rtx-3080'

page = requests.get(scrape_url)

from alternate import AlternateFetcher
from caseking import CasekingFetcher

fetcher1 = AlternateFetcher()
entries1 = fetcher1.fetch(page.content)

fetcher2 = CasekingFetcher()
entries2 = fetcher2.fetch(requests.get(scrape2).content)

from database import Database
from discord_bot import DiscordBot

hook_url = open('webhook.url', 'r').readline()

bot = DiscordBot(hook_url)

db = Database('data.db')
# db.create_database()
db.register_listener(bot)

db.update(entries1)
db.update(entries2)

pass

db.save()