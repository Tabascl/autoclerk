import json
from concurrent.futures.thread import ThreadPoolExecutor

import requests

import fetchers


class FetcherHandler():
    def __init__(self, sites_json):
        sites = json.load(open(sites_json, 'r'))

        self.workers = []

        for fetcher in fetchers.FETCHER_LIST:
            if fetcher.NAME in sites.keys():
                url = sites[fetcher.NAME]['url']
                self.workers.append((fetcher(), url))

    def start(self):
        with ThreadPoolExecutor(max_workers=5) as pool:
            result = list(pool.map(self.fetch_site, self.workers))

        return [product for sublist in result for product in sublist]

    def fetch_site(self, worker):
        return worker[0].fetch(worker[1])
