from typing import List

from product import Product


class IFetcher:
    def fetch(self, link) -> List[Product]:
        pass
