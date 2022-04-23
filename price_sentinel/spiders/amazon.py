"""
Module based on github/stummjr's scrapy-price-monitor project
Found on https://github.com/stummjr/scrapy_price_monitor/
"""
from .base_spider import BaseSpider


class AmazonSpider(BaseSpider):
    name = "amazon.com"

    def parse(self, response):
        item = response.meta.get('item-meta', {})
        item['title'] = response.css("span#productTitle::text").extract_first("").strip()
        price = response.css('span.a-offscreen::text').get()
        item['price'] = price

        yield item