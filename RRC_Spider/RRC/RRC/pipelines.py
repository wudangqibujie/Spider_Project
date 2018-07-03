# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from RRC.items import Infotem,ReportItem
import pymongo
class RRCPipeline(object):
    def open_spider(self,spider):
        self.client = pymongo.MongoClient()
        self.db = self.client["RRC_Scrapy"]
    def process_item(self, item, spider):
        if isinstance(item,Infotem):
            self.db["info_data"].insert(dict(item))
        if isinstance(item,ReportItem):
            self.db["report_data"].insert(dict(item))
        return item
    def close_spider(self,spider):
        self.client.close()