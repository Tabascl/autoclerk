import requests
from bs4 import BeautifulSoup
import re

from fetcher_handler import FetcherHandler

handler = FetcherHandler('sites.json')
entries = handler.start()

from database import Database
from discord_bot import DiscordBot

hook_url = open('webhook.url', 'r').readline()

bot = DiscordBot(hook_url)

db = Database('data.db')
# db.create_database()
db.register_listener(bot)

db.update(entries)

pass

db.save()