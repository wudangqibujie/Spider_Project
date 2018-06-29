# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy
class CityItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city_name = scrapy.Field()
    city_link = scrapy.Field()
class DetailItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    base_info = scrapy.Field()
    address = scrapy.Field()
    price = scrapy.Field()
    uni_price = scrapy.Field()
















