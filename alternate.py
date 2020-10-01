import re
from typing import List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from fetcher_interface import IFetcher
from product import Product

NAME = 'Alternate.de'
DOMAIN = 'https://www.alternate.de'


class AlternateFetcher(IFetcher):
    def fetch(self, html) -> List[Product]:
        soup = BeautifulSoup(html, 'html.parser')

        products = soup.find_all('div', class_='listRow')

        entries = []
        for product in products:
            try:
                entries.append(self._get_product_info(product))
            except AttributeError:
                "Missing something, skip"

        return entries

    def _get_product_info(self, product):
        name_span = product.find('span', class_='name')
        stock_span = product.find(
            'span', class_=re.compile('stockStatus*'))
        price_span = product.find('span', class_=re.compile('price*'))

        name = name_span.get_text().strip()
        availability = stock_span.get_text().strip()

        print("Alternate: Gathering info for {}".format(name[:20] + "..."))

        price = price_span.get_text()
        price = float(re.search('\s([0-9]*),', price).group(1))

        product_link = self._extract_product_link(product)

        ean = self._extract_ean(product_link)

        return Product(ean, name, NAME, availability, price, product_link)

    def _extract_product_link(self, product):
        product_link = product.find('a', class_='productLink')
        return urljoin(DOMAIN, product_link['href'])

    def _extract_ean(self, product_link):
        product_html = requests.get(product_link).content

        soup = BeautifulSoup(product_html, 'html.parser')

        return soup.find('td', text='EAN').find_next_sibling('td').get_text().strip()
