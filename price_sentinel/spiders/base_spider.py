"""
Module based on github/stummjr's scrapy-price-monitor project
Found on https://github.com/stummjr/scrapy_price_monitor/
"""
import os
import scrapy
import locale
from datetime import datetime
import yaml
from yaml.loader import SafeLoader


# Open the file and load the file
PRODUCTS_DIR = "resources"
FILE_NAME = "products.yml"

class BaseSpider(scrapy.Spider):
    def start_requests(self):
        ROOT_DIR = os.environ["PRICE_SENTINEL_ROOT_DIR"]
        products_path = os.path.join(ROOT_DIR, PRODUCTS_DIR, FILE_NAME)

        with open(products_path) as f:
            products = yaml.load(f, Loader=SafeLoader)
            
        for product_id, product_info in products.items():

            for url in product_info["urls"]:
                if self.name in url:
                    now = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                    item = {'product_name': product_info["name"],
                            'retailer': self.name, 
                            'when': now}
                    yield scrapy.Request(url, meta={'item': item})