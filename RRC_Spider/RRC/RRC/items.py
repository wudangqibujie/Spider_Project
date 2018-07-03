# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Infotem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    car_id = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    city = scrapy.Field()
    year_age = scrapy.Field()
    price = scrapy.Field()
class ReportItem(scrapy.Item):
    car_id = scrapy.Field()
    option_name = scrapy.Field()
    option_counts = scrapy.Field()
    fetal_counts = scrapy.Field()




















