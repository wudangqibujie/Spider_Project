from req import Aio_Req,Sin_Req
from lxml import etree
import asyncio
from settings import *
import threading as th
from m_queue import TaskQueue
import requests
import json
from task import tasks
from log import log
from urllib.parse import urljoin
from db import Mon
task_queue = TaskQueue()
mon = Mon()
class Lj_Zf_Spider(object):
    def __init__(self):
        self.tasks = tasks
    def start_req(self):
        for i in tasks:
            base_link = i+"zufang/pg{}/"
            page = 1
            task_queue.add_task(Aio_Req(base_link.format(page),self.parse_item,meta={"page":page,"base_link":base_link}))
    def parse_item(self,response):
        html = etree.HTML(response["response"])
        page = response["page"]
        base_link = response["base_link"]
        items = html.xpath('//ul[@class="house-lst"]/li')
        next_item = html.xpath('//div[@comp-module="page"]/@page-data')
        log.log("下一页item   "+str(next_item),"debug")
        if next_item:
            next_data = eval(next_item[0])
            if int(next_data["totalPage"]) >= page:
                log.log(("总页数   "+str(next_data["totalPage"])+"   "+"现在页数   "+str(page)),"debug")
                log.log(str(items),"debug")
                if items:
                    for j in items:
                        data = dict()
                        title = j.xpath('div[@class="info-panel"]/h2/a/@title')
                        data["title"] = title
                        data["city"] = j.xpath('//title/text()')
                        link = j.xpath('div[@class="pic-panel"]/a/@href')
                        data["link"] = link
                        name = j.xpath('div[@class="info-panel"]/div[@class="col-1"]/div[@class="where"]/a/span/text()')
                        if not name:
                            name = j.xpath('div[@class="info-panel"]/div[@class="col-1"]/div[@class="where"]/span[@class="region"]/text()')
                        data["name"] = name
                        sty_size = j.xpath('div[@class="info-panel"]/div[@class="col-1"]/div[@class="where"]/span[@class="meters"]/text()')
                        data["size"] = sty_size
                        data["price"] = j.xpath('div[@class="info-panel"]/div[@class="col-3"]/div[@class="price"]/span/text()')
                        data["address"] = j.xpath('div[@class="info-panel"]/div[@class="col-1"]/div[@class="other"]/div[@class="con"]/a/text()')
                        log.log(str(data),"info")
                        mon.insert("zufang",data)
                    task_queue.old_task(base_link.format(page))
                    task_queue.add_task(Aio_Req(base_link.format(page+1),callback=self.parse_item,meta={"page":page,"base_link":base_link}))
    def run(self,nums):
        while True:
            task_ = [task_queue.pop_task() for _ in range(nums)]
            tasks = [i.aio_req() for i in task_ if i != None]
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(tasks))
            if None in task_:
                log.log("任务队列已空！","info")
                break
if __name__ == '__main__':
    a = Lj_Zf_Spider()
    # a.start_req()
    a.run(CON_NUMS)
