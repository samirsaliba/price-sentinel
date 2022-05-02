"""
Module based on github/stummjr's scrapy-price-monitor project
Found on https://github.com/stummjr/scrapy_price_monitor/
"""
import os
import scrapy
from datetime import datetime
import json
from ..items import PriceSentinelItem

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
                    meta = {'name': product_id,
                            'retailer': self.name, 
                            'timestamp': now,
                            'url': url}
                    yield scrapy.Request(url, meta={'item-meta': meta})

    def initialize_object(self, response):
        item = PriceSentinelItem()
        meta = response.meta.get('item-meta', {})        
        item.update(meta)
        return item

