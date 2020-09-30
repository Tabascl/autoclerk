import requests
from bs4 import BeautifulSoup
import re

scrape_url = 'https://www.alternate.de/Grafikkarten/RTX-3080'

page = requests.get(scrape_url)

from alternate import AlternateFetcher

fetcher = AlternateFetcher()
entries = fetcher.fetch(page.content)

from database import Database
from discord_bot import DiscordBot

bot = DiscordBot('')

db = Database('data.db')
db.register_listener(bot)

db.create_database()
db.update(entries)

pass

db.save()