#!/usr/bin/env python3
import argparse

from database import Database
from discord_bot import DiscordBot
from fetcher_handler import FetcherHandler

hook_url = open('webhook.url', 'r').readline()
bot = DiscordBot(hook_url)

db = Database('data.db')
db.register_listener(bot)

parser = argparse.ArgumentParser()

create_db = False
parser.add_argument('-c', dest='create_db', action='store_true')

args = parser.parse_args()

if args.create_db:
    db.create_database()

handler = FetcherHandler('sites.json')
entries = handler.start()

db.update(entries)

db.save()

print("Done!")
