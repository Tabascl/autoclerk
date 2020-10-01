import argparse

from database import Database
from discord_bot import DiscordBot
from fetcher_handler import FetcherHandler

hook_url = open('webhook.url', 'r').readline()
bot = DiscordBot(hook_url)

db = Database('data.db')
db.register_listener(bot)

def create_database():
    db.create_database()

parser = argparse.ArgumentParser()
parser.add_argument('-c', action='create_database')

parser.parse_args()

handler = FetcherHandler('sites.json')
entries = handler.start()

db.update(entries)

db.save()

print("Done!")
