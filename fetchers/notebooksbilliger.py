import re
from typing import List

import requests
from bs4 import BeautifulSoup

from fetchers.fetcher_interface import IFetcher
from product import Product

HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63"}


class NotebooksBilligerFetcher(IFetcher):
    NAME = 'Notebooksbilliger.de'

    def fetch(self, link) -> List[Product]:
        html = requests.get(link, headers=HEADER).content
        soup = BeautifulSoup(html, 'html.parser')

        products = soup.find_all('div', class_='js-ado-product-click')

        entries = []
        for product in products:
            try:
                entries.append(self._get_product_info(product))
            except AttributeError:
                print("Erratic product")

        return entries

    def _get_product_info(self, product):
        name_link = product.find('a', class_='listing_product_title')
        stock_div = product.find(
            'div', class_='availability_info')
        price_span = product.find('span', class_='product-price__regular')

        name = name_link.get_text().strip()
        availability = stock_div.get_text().strip()

        print("{}: Gathering info for {}".format(self.NAME, name[:20] + "..."))

        price = price_span.get_text().strip()
        price = re.search('^([0-9,.]*),', price).group(1)
        price = re.sub('\.', '', price)
        price = float(re.sub(',', '.', price))

        product_link = self._extract_product_link(product)

        ean = self._extract_ean(product_link)

        return Product(ean, name, self.NAME, availability, price, product_link)

    def _extract_product_link(self, product):
        return product.find('a', class_='listing_product_title')['href']

    def _extract_ean(self, product_link):
        product_html = requests.get(product_link, headers=HEADER).content

        soup = BeautifulSoup(product_html, 'html.parser')

        return soup.find('div', text='EAN-Nummer').parent.find_next_sibling('td').find('div').get_text().strip()
