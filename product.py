class Product:
    def __init__(self, ean: str, name: str, shop: str, availability: str, price: float, product_link: str):
        self.ean = ean
        self.name = name
        self.shop = shop
        self.availability = availability
        self.price = price
        self.product_link = product_link
