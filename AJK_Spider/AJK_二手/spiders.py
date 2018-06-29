from req import Aio_Req,Sin_Req
from lxml import etree
import asyncio
from settings import *
import threading as th
from m_queue import TaskQueue
import requests
import json
from log import log
import task
from urllib.parse import urljoin
from db import Mon
task_queue = TaskQueue()
mon = Mon()
class Ajk_es_Spider(object):
    def __init__(self):
        self.task = task.tasks
    def start_req(self):
        """
        任务的初始化
        :return:把初始任务url封装成Request放入任务队列
        """
        for k in self.task.keys():
            city = k
            link = self.task[city]
            task_queue.add_task(Sin_Req(link+r'sale/',self.parse_items,meta={"city":city}))
    def parse_items(self,response):
        """
        解析出列表页的数据
        :param response:来自列表页的响应数据
        :return:对存在下一页的连接重新封装成放入待爬取队列，解析出的数据持久化至MongoDB
        """
        html = etree.HTML(response["response"])
        city = response["city"]
        item_data = html.xpath('//ul[@id="houselist-mod-new"]/li')
        next_item = html.xpath('//div[@class="multi-page"]/a')
        if next_item:
            if "下一页" in next_item[-1].xpath('text()')[0]:
                next_url = next_item[-1].xpath('@href')
                if next_url:
                    log.log("下一页链接   "+next_url[0],"debug")
                    next_task =Sin_Req(next_url[0],self.parse_items,meta={"city":city})
                    task_queue.add_task(next_task)
        if item_data:
            for i in item_data:
                item = dict()
                item["city"] = city
                item["title"] = i.xpath('div[@class="house-details"]/div[1]/a/@title')
                item["link"] = i.xpath('div[@class="house-details"]/div[1]/a/@href')
                item["room_style"] = i.xpath('div[@class="house-details"]/div[2]/span[1]/text()')
                item["size"] = i.xpath('div[@class="house-details"]/div[2]/span[2]/text()')
                item["price"] = i.xpath('div[@class="pro-price"]/span[@class="price-det"]/strong/text()')
                item["uni_price"] = i.xpath('div[@class="pro-price"]/span[@class="unit-price"]/text()')
                item["year"] = i.xpath('div[@class="house-details"]/div[2]/span')[-2].xpath('text()')
                item["name_location"] =i.xpath('div[@class="house-details"]/div[3]/span/@title')
                log.log(str(item),"info")
                mon.insert("ajk_ershou",item)
    def run(self,nums):
        """
        :param nums:并发数
        :return:
        """
        while True:
            task_ = [task_queue.pop_task() for _ in range(nums)]
            tasks = [th.Thread(target=i.get()) for i in task_ if i != None]
            for i in tasks:
                i.start()
            for i in tasks:
                i.join()
            if None in task_:
                log.log("任务队列已空！","info")
                break
if __name__ == '__main__':
    a = Ajk_es_Spider()
    a.start_req()
    a.run(CON_NUMS)
