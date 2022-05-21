# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import os
import pymysql
import locale


class PriceSentinelPipeline:

    def __init__(self) -> None:
        self.HOST = os.environ["DB_HOST"]
        self.USER = os.environ["DB_USER"]
        self.PASSWORD = os.environ["DB_PASSWORD"]
        self.PORT = os.getenv('DB_PORT', None)
        if self.PORT is not None:
            self.PORT = int(self.PORT)
        self.DATABASE = os.environ["DB_DATABASE"]
        self.TABLE = os.environ["DB_TABLE"]

        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = pymysql.connect(host=self.HOST,
                                    user=self.USER,
                                    password=self.PASSWORD,
                                    database=self.DATABASE,
                                    port=self.PORT)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.DATABASE}.{self.TABLE}
            (`name` VARCHAR(50),
            `title` VARCHAR(200),
            `price` DECIMAL(10,2),
            `retailer` VARCHAR(50),
            `timestamp` DATETIME);
            """
        )

    def process_price(self, item):
        if ("R$" in item["price"]) or (".br" in item["url"]):
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
            money = item["price"].strip("R$")

        else:
            locale.setlocale(locale.LC_ALL, 'en_US.utf8')
            money = item["price"].strip("$")

        return locale.atof(money)

    def store_item_in_db(self, item):
        sql = f"""
            INSERT INTO {self.DATABASE}.{self.TABLE}
            (`name`, `title`, `price`, `retailer`, `timestamp`)
            VALUES (%s, %s, %s, %s, %s);
            """
        values = (item["name"], item["title"],
                  item["price"], item["retailer"],
                  item["timestamp"])
        self.cursor.execute(sql, values)
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

    def process_item(self, item, spider):
        item["price"] = self.process_price(item)
        item["title"] = item["title"][0:200]
        self.store_item_in_db(item)
        return item