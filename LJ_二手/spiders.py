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
class Lj_Es_Spider(object):
    def __init__(self):
        self.tasks = tasks
    def start_req(self):
        """
        初始化请求
        :return:
        """
        for i in tasks:
            base_link = i+"ershoufang/pg{}/"
            page = 1
            task_queue.add_task(Aio_Req(base_link.format(page),self.parse_item,meta={"page":page,"base_link":base_link}))
    def parse_item(self,response):
        """
        :param response:返回初始请求的响应HTML
        :return:构造下一页的请求和解析出的数据进行持久化保存
        """
        html = etree.HTML(response["response"])
        page = response["page"]
        base_link = response["base_link"]
        items = html.xpath('//ul[@class="sellListContent"]/li')
        next_item = html.xpath('//div[@comp-module="page"]/@page-data')
        if not next_item:
            print(response["response"])
        log.log("下一页item   "+str(next_item),"debug")
        if next_item:
            next_data = eval(next_item[0])
            if int(next_data["totalPage"]) >= page:
                log.log(("总页数   "+str(next_data["totalPage"])+"   "+"现在页数   "+str(page)),"debug")
                log.log(str(items),"debug")
                if items:
                    for j in items:
                        data = dict()
                        title = j.xpath('a/img/@alt')
                        data["city"] = j.xpath('//title/text()')
                        data["title"] = title
                        link = j.xpath('a/@href')
                        data["link"] = link
                        name = j.xpath('div[@class="info clear"]/div[@class="address"]/div[@class="houseInfo"]/a/text()')
                        data["name"] = name
                        sty_size = j.xpath('div[@class="info clear"]/div[@class="address"]/div[@class="houseInfo"]/text()')
                        data["size"] = sty_size
                        data["uni_price"] = j.xpath('div[@class="info clear"]/div[@class="priceInfo"]/div[2]/@data-price')
                        data["price"] = j.xpath('div[@class="info clear"]/div[@class="priceInfo"]/div[1]/span/text()')
                        log.log(str(data),"info")
                        mon.insert("ershou",data)
                    task_queue.old_task(base_link.format(page))
                    task_queue.add_task(Aio_Req(base_link.format(page+1),callback=self.parse_item,meta={"page":page,"base_link":base_link}))
    def run(self,nums):
        """
        :param nums:并发数
        :return:
        """
        while True:
            task_ = [task_queue.pop_task() for _ in range(nums)]
            tasks = [i.aio_req() for i in task_ if i != None]
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(tasks))
            if None in task_:
                log.log("任务队列已空！","info")
                break
if __name__ == '__main__':
    a = Lj_Es_Spider()
    a.start_req()
    a.run(CON_NUMS)
