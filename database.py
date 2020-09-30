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

    def _pricepoint_insert(self, values):
        self.connection.execute(
            '''INSERT INTO pricepoint (time, product_ean, price)
               VALUES (?, ?, ?)''', values
        )

    def _insert(self, product):
        print("New product, inserting")

        self.connection.execute(
            '''INSERT INTO product (ean, name, availability, product_link) 
               VALUES (?, ?, ?, ?)''', (product.ean, product.name, product.availability, product.product_link))

        now = int(time.time())
        self._pricepoint_insert((now, product.ean, product.price))

        self.notify(InsertEvent(product))

    def _update(self, db_record, product):
        if db_record[1] != product.price:
            print(
                "Price change detected: {} -> {}".format(db_record[1], product.price))

            now = int(time.time())
            self._pricepoint_insert((now, product.ean, product.price))

            self.notify(PriceEvent(db_record[1], product))

        if db_record[2] != product.availability:
            print(
                "Availability change detected: {} -> {}".format(db_record[2], product.availability))

            self.connection.execute(
                '''UPDATE product
                SET availability = ?
                WHERE ean = ?''', (product.availability, product.ean))

            self.notify(AvailabilityEvent(db_record[2], product))

    def update(self, products: List[Product]):
        cursor = self.connection.execute(
            '''SELECT product_ean, price, availability
               FROM pricepoint 
               JOIN product ON product_ean = ean 
               GROUP BY product_ean 
               HAVING time = max(time)''')
        latest_data = cursor.fetchall()

        for product in products:
            if product.ean not in [row[0] for row in latest_data]:
                self._insert(product)
            else:
                self._update(
                    next(row for row in latest_data if row[0] == product.ean), product)

    def save(self):
        self.connection.commit()
