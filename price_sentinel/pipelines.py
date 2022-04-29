# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import os
import pymysql


class PriceSentinelPipeline:

    def __init__(self) -> None:
        self.HOST = os.environ["HOST"]
        self.USER = os.environ["USER"]
        self.PASSWORD = os.environ["PASSWORD"]
        self.PORT = os.getenv('PORT', None)
        self.DATABASE = os.environ["DATABASE"]
        self.TABLE = os.environ["TABLE"]

        self.create_connection()
        self.create_table()

        pass

    def check_if_table_exists(self):
        sql = f"""
            SELECT COUNT(*) from information_schema.`TABLES` AS t 
            WHERE t.`TABLE_SCHEMA` = "{self.DATABASE}" 
            AND t.table_name = "{self.TABLE}" 
            """
        self.cursor.execute(sql)
        if self.cursor.fetchone()[0] == 0:
            return False
        return True

    def create_connection(self):
        self.conn = pymysql.connect(host=self.HOST,
                                    user=self.USER,
                                    password=self.PASSWORD,
                                    database=self.DATABASE,
                                    port=self.PORT)
        self.cursor = self.conn.cursor()
        

    def create_table(self):
        self.cursor.execute()
        pass

    def process_price(value):
        return value

    def store_item_in_db(item):
        pass

    def close_connection(self):
        self.conn.close()

    def process_item(self, item, spider):
        item["price"] = self.process_price(item["price"])
        self.store_item_in_db(item)
        return item
