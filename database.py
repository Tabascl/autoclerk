import sqlite3
import time
from typing import List

from fetcher_interface import ProductUpdate


class Database():
    def __init__(self, file):
        self.connection = sqlite3.connect(file)

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
        self.connection.execute(
            '''INSERT INTO product (ean, name, availability) 
               VALUES (?, ?, ?)''', (product.ean, product.name, product.availability))

        now = int(time.time())
        self._pricepoint_insert((now, product.ean, product.price))

    def _update(self, db_record, product):
        if db_record[1] != product.price:
            print("Price change detected: {} -> {}".format(product.price, db_record[1]))

            now = int(time.time())
            self._pricepoint_insert((now, product.ean, product.price))
        
        if db_record[2] != product.availability:
            print("Availability change detected: {} -> {}".format(product.availability, db_record[2]))
            self.connection.execute(
                '''UPDATE product
                SET availability = ?
                WHERE ean = ?''', (db_record[2], product.ean))

    def update(self, products: List[ProductUpdate]):
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
