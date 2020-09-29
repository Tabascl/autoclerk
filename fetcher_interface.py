from typing import List

class ProductUpdate:
    def __init__(self, ean: str, name: str, availability: str, price: float):
        self.ean = ean
        self.name = name
        self.availability = availability
        self.price = price

class IFetcher:
    def fetch(self, html) -> List[ProductUpdate]:
        pass