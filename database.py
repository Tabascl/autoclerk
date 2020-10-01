import sqlite3
import time
from typing import List

from events import *
from product import Product


class Database():
    def __init__(self, file):
        self.connection = sqlite3.connect(file)
        self.listeners = []

    def register_listener(self, listener):
        self.listeners.append(listener)

    def notify(self, event):
        for listener in self.listeners:
            listener.update(event)

    def create_database(self):
        with open('init.sql', 'r') as sql_file:
            sql_script = sql_file.read()

        self.connection.executescript(sql_script)

    def _new_product(self, product: Product):
        self.connection.execute(
            '''INSERT INTO Product (EAN, Name) VALUES (?, ?)''', (product.ean, product.name))

    def _get_product_id(self, product: Product):
        cursor = self.connection.execute(
            '''SELECT Product.Product_Id
               FROM Product
               WHERE Product.EAN = ?''', (product.ean,)
        )

        return cursor.fetchone()[0]

    def _get_shop_id(self, product: Product):
        cursor = self.connection.execute(
            '''SELECT Shop.Shop_Id
               FROM Shop
               WHERE Shop.Name = ?''', (product.shop,)
        )

        return cursor.fetchone()[0]

    def _insert_sell(self, product: Product):
        product_id = self._get_product_id(product)
        shop_id = self._get_shop_id(product)

        self.connection.execute(
            '''INSERT INTO sells (Product_Id, Shop_Id, Availability, Link)
               VALUES(?, ?, ?, ?)''', (product_id, shop_id, product.availability, product.product_link)
        )

        self.notify(InsertEvent(product))

    def _update_sell(self, product: Product, availability):
        product_id = self._get_product_id(product)
        shop_id = self._get_shop_id(product)

        if availability != product.availability:
            self.connection.execute(
                '''UPDATE sells
                   SET availability = ?
                   WHERE product_id = ? AND shop_id = ?''', (product.availability, product_id, shop_id)
            )

            self.notify(AvailabilityEvent(availability, product))

    def _process_sell(self, product: Product):
        cursor = self.connection.execute(
            '''SELECT sells.availability 
            FROM sells
            JOIN Product ON sells.Product_Id = Product.Product_Id
            JOIN Shop ON sells.Shop_Id = Shop.Shop_Id
            WHERE Product.EAN = ? AND Shop.Name = ?''', (product.ean, product.shop)
        )

        availability = cursor.fetchone()

        if not availability:
            self._insert_sell(product)
        elif availability[0] != product.availability:
            self._update_sell(product, availability[0])

    def _notify_ask(self, product, old_price):
        cursor = self.connection.execute(
            '''SELECT Price
               FROM asks
               WHERE Product_Id =
               (SELECT Product_Id
                FROM Product
                WHERE Product.EAN = ?)
               GROUP BY Shop_Id
               HAVING MAX(Time)''', (product.ean,)
        )

        latest_prices = cursor.fetchall()

        if all([product.price <= price[0] for price in latest_prices]):
            new_lowest = True
        else:
            new_lowest = False

        self.notify(PriceEvent(old_price, product, new_lowest))
        

    def _process_ask(self, product: Product):
        cursor = self.connection.execute(
            '''SELECT MAX(asks.Time), asks.Price
               FROM asks
               JOIN Product ON asks.Product_Id = Product.Product_Id
               JOIN Shop ON asks.Shop_Id = Shop.Shop_Id
               WHERE Product.EAN = ? AND Shop.Name = ?''', (product.ean, product.shop)
        )

        price = cursor.fetchone()[1]

        if price != product.price:
            product_id = self._get_product_id(product)
            shop_id = self._get_shop_id(product)
            now = int(time.time())

            self.connection.execute(
                '''INSERT INTO asks (Product_Id, Shop_Id, Price, Time)
                   VALUES (?, ?, ?, ?)''', (product_id, shop_id, product.price, now)
            )

            if not price:
                price_override = 0
            else:
                price_override = price

            self._notify_ask(product, price_override)

    def update(self, products: List[Product]):
        # Make sure the Shop exists
        self.connection.executemany('''INSERT OR IGNORE INTO Shop (Name) VALUES (?)''', [(product.shop,) for product in products])

        cursor = self.connection.execute(
            '''SELECT EAN from Product''')
        eans = [ean[0] for ean in cursor.fetchall()]

        for product in products:
            if product.ean not in eans:
                self._new_product(product)

        for product in products:
            self._process_sell(product)
            self._process_ask(product)


    def save(self):
        self.connection.commit()
