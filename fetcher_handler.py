import json

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
        products = []

        for worker in self.workers:
            html = requests.get(worker[1]).content
            products += worker[0].fetch(html)

        return products
