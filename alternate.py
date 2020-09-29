import re
from typing import List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from fetcher_interface import IFetcher, ProductUpdate

DOMAIN = 'https://www.alternate.de'


class AlternateFetcher(IFetcher):
    def fetch(self, html) -> List[ProductUpdate]:
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

        print("Gathering info for {}".format(name[:20] + "..."))

        price = price_span.get_text()
        price = float(re.search('\s([0-9]*),', price).group(1))

        ean = self._extract_ean(product)

        return ProductUpdate(ean, name, availability, price)

    def _extract_ean(self, product):
        product_link = product.find('a', class_='productLink')
        absolute_url = urljoin(DOMAIN, product_link['href'])
        product_html = requests.get(absolute_url).content

        soup = BeautifulSoup(product_html, 'html.parser')

        return soup.find('td', text='EAN').find_next_sibling('td').get_text().strip()
