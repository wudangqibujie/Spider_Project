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
class AK_Spider(object):
    def __init__(self):
        self.cars = task.tasks
    def start_req(self):
        """
        初始化任务队列
        :return:
        """
        for k in self.cars.keys():
            car_name = k
            car_base_link = self.cars[k]
            task_queue.add_task(Sin_Req(car_base_link,self.parse_items,meta={"car":car_name}))
    def parse_items(self,response):
        """
        帖子的抓取
        :param response:
        :return:
        """
        html = etree.HTML(response["response"])
        items = html.xpath('//dl[@class="list_dl"]')
        next_items = html.xpath('//a[@class="page_down"]/@href')
        log.log(str(items),"debug")
        car_name = response["car"]
        if next_items:
            if items:
                for i in items:
                    data = {}
                    title = i.xpath('dt/p[@class="thenomal"]/a/text()')
                    link = i.xpath('dt/p[@class="thenomal"]/a/@href')
                    post_time = i.xpath('dd[@class="w98"]/span[@class="tdate"]/text()')
                    comment_nums = i.xpath('dd[@class="cli_dd"]/span[@class="fontblue"]/text()')
                    views_nums = i.xpath('dd[@class="cli_dd"]/span[@class="tcount"]/text()')
                    data["car"] = car_name
                    data["title"] = title
                    data["link"] = link
                    data["post_time"] = post_time
                    data["comment_nums"] = comment_nums
                    data["views_nums"] = views_nums
                    log.log(str(data),"info")
                    mon.insert("data",data)
            next_link = "http://www.xcar.com.cn/bbs/"+next_items[0]
            log.log("下一页连接  "+next_link,"debug")
            task_queue.add_task(Sin_Req(next_link,self.parse_items,meta={"car":car_name}))
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
    a = AK_Spider()
    a.start_req()
    a.run(CON_NUMS)
