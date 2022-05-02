# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PriceSentinelItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    retailer = scrapy.Field()
    timestamp = scrapy.Field()
    url = scrapy.Field()
    

    
