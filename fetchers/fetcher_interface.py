from typing import List

from product import Product


class IFetcher:
    def fetch(self, html) -> List[Product]:
        pass
