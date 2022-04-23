"""
Module based on github/stummjr's scrapy-price-monitor project
Found on https://github.com/stummjr/scrapy_price_monitor/
"""
import os
import scrapy
from datetime import datetime
import json


# Open the file and load the file
FILE_NAME = "products.json"

class BaseSpider(scrapy.Spider):
    def start_requests(self):
        ROOT_DIR = os.environ["RESOURCES_DIR"]
        products_path = os.path.join(ROOT_DIR, FILE_NAME)

        with open(products_path) as file:
            products = json.load(file)

        for product_id, product_urls in products.items():
            for url in product_urls:
                if self.name in url:
                    now = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                    meta = {'product_name': product_id,
                            'retailer': self.name, 
                            'when': now,
                            'url': url}
                    yield scrapy.Request(url, meta={'item-meta': meta})