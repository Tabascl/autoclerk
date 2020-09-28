import sqlite3
import time

class Database():
    def __init__(self, file):
        self.connection = sqlite3.connect(file)

    def create_database(self):
        with open('init.sql', 'r') as sql_file:
            sql_script = sql_file.read()

        self.connection.executescript(sql_script)

    def insert_product(self, values):
        self.connection.execute('INSERT INTO product VALUES (?, ?, ?)', values)

    def insert_price(self, values):
        with_time = (int(time.time()),)
        with_time += values
        self.connection.execute('INSERT INTO pricepoint (time, product_ean, price) VALUES (?, ?, ?)', with_time)

    def save(self):
        self.connection.commit()
