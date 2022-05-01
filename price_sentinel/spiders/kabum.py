"""
Module based on github/stummjr's scrapy-price-monitor project
Found on https://github.com/stummjr/scrapy_price_monitor/
"""
from .base_spider import BaseSpider
import unidecode


class KabumSpider(BaseSpider):
    name = "kabum.com"

    def parse(self, response):
        item = self.initialize_object(response)

        item['title'] = response.css('h1[itemprop="name"]::text').get()
        price = response.css('h4[itemprop="price"]::text').get()
        item['price'] = unidecode.unidecode(price)

        yield item