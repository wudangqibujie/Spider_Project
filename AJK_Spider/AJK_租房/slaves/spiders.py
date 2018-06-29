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
class Ajk_zf_Spider(object):
    def __init__(self):
        self.task = task.tasks
    def start_req(self):
        for k in self.task.keys():
            city = k
            link = self.task[city].replace(r'anjuke',r'zu.anjuke')
            task_queue.add_task(Sin_Req(link,self.parse_items,meta={"city":city}))
    def parse_items(self,response):
        html = etree.HTML(response["response"])
        city = response["city"]
        item_data = html.xpath('//div[@class="zu-itemmod  "]')
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
                item["title"] = i.xpath('a/@title')
                item["link"] = i.xpath('a/@href')
                item["size_style"] = i.xpath('div[@class="zu-info"]/p[@class="details-item tag"]/span[1]/text()')
                item["price"] = i.xpath('div[@class="zu-side"]/p/strong/text()')
                item["name"] =i.xpath('div[@class="zu-info"]/address/a/text()')
                item["address"] = i.xpath('div[@class="zu-info"]/address/text()')
                log.log(str(item),"info")
                mon.insert("ajk_zufang",item)
    def run(self,nums):
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
    a = Ajk_zf_Spider()
    # a.start_req()
    a.run(CON_NUMS)
