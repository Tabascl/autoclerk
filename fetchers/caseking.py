import re
from typing import List

import requests
from bs4 import BeautifulSoup

from fetchers.fetcher_interface import IFetcher
from product import Product


class CasekingFetcher(IFetcher):
    NAME = 'Caseking.de'

    def fetch(self, html) -> List[Product]:
        soup = BeautifulSoup(html, 'html.parser')

        products = soup.find_all('div', class_='artbox')

        products = self._get_page_products(html)

        entries = []

        for product in products:
            try:
                entry = self._get_product_info(product)
            except AttributeError:
                print("Probably hit the search fallback if this occurs only once")
                continue

            if entry:
                entries.append(entry)

        return entries

    def _get_page_products(self, html, products=[]):
        soup = BeautifulSoup(html, 'html.parser')
        next_page = soup.select('a.navi.more')

        if not next_page:
            return soup.find_all('div', class_='artbox')
        else:
            next_page_link = next_page[0]['href']
            return soup.find_all('div', class_='artbox') + self._get_page_products(requests.get(next_page_link).content)

    def _get_product_info(self, product):
        name_first = product.find('span', class_='ProductSubTitle')
        name_second = product.find('span', class_='ProductTitle')

        name = "{} {}".format(name_first.get_text().strip(),
                              name_second.get_text().strip())

        print("{}: Gathering info for {}".format(self.NAME, name[:20] + "..."))

        availability_span = product.find(
            'span', class_='frontend_plugins_index_delivery_informations')
        availability = availability_span.get_text().strip()

        price_span = product.find('span', class_='price')
        price = price_span.get_text().strip()
        price = re.search('^([0-9,]*)', price).group(1)
        price = float(re.sub(',', '.', price))

        product_link = product.find('a', class_='producttitles')['href']
        ean = self._extract_ean(product_link)

        if re.search('^0*$', ean):
            return None
        else:
            return Product(ean, name, self.NAME, availability, price, product_link)

    def _extract_ean(self, product_link):
        product_html = requests.get(product_link).content

        soup = BeautifulSoup(product_html, 'html.parser')

        text = soup.find('span', class_='frontend_detail_index',
                         text='EAN:').parent.get_text().strip()
        return re.sub('EAN: ', '', text)
