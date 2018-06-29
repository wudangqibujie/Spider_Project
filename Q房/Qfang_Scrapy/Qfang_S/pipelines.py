# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from Qfang_S.items import CityItem,DetailItem
import pymongo
class QFPipeline(object):
    def open_spider(self,spider):
        self.client = pymongo.MongoClient()
        self.db = self.client["QF_Scrapy"]
    def process_item(self, item, spider):
        if isinstance(item,CityItem):
            self.db["city_data"].insert(dict(item))
        if isinstance(item,DetailItem):
            self.db["detail_data"].insert(dict(item))
        return item

    def close_spider(self,spider):
        self.client.close()