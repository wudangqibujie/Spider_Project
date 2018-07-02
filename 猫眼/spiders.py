from req import Aio_Req,Sin_Req,Bin_Req
from lxml import etree
import asyncio
import re
from settings import *
import threading as th
import filter_word
from m_queue import TaskQueue
import requests
import time
import json
from log import log
from urllib.parse import urljoin
from db import Mon
task_queue = TaskQueue()
mon = Mon()
class YX_Spider(object):
    def __init__(self):
        self.base_url = "http://maoyan.com/cinemas?offset={}"
    def start_req(self):
        for i in range(22):#22
            task_link = self.base_url.format(i*12)
            task_queue.add_task(Sin_Req(task_link,self.parse_items))
    def parse_items(self,response):
        wo_url = "http://" + re.findall(r"url.*?//(.*?)'.*?format.*?woff", response["response"])[0]
        html = etree.HTML(response["response"])
        items = html.xpath('//div[@class="cinema-cell"]')
        aaa = html.xpath('//span[@class="stonefont"]/text()')
        print(wo_url)
        data_lst = []
        for i in items:
            data = dict()
            name = i.xpath('div[@class="cinema-info"]/a/text()')
            address = i.xpath('div[@class="cinema-info"]/p/text()')
            price = i.xpath('div[@class="price"]/span[@class="price-num red"]/span/text()')[0]
            data["name"] = name
            data["address"] = address
            data["price"] = price
            data = str(data).replace(r'\u',"uni")
            data = eval(data)
            data_lst.append(data)
        task_queue.add_task(Bin_Req(wo_url,self.parse_woff,meta={"data":data_lst}))
    def parse_woff(self,response):
        data = response["data"]
        aa = filter_word.rule_(response["response"])
        log.log(str(aa),"debug")
        for i in data:
            if "." not in i["price"]:
                real_price = aa[i["price"][0:7]]+aa[i["price"][7:15]]
                i["price"] = real_price
            else:
                real_price = aa[i["price"][0:7]] + aa[i["price"][7:14]] + "." + aa[i["price"][15:22]]
                i["price"] = real_price
            log.log(str(i),"info")
            mon.insert("data",i)
    def run(self,nums):
        while True:
            task_ = [task_queue.pop_task() for _ in range(nums)]
            tasks = [th.Thread(target=i.get()) for i in task_ if i != None]
            for i in tasks:
                i.start()
                time.sleep(1)
            for i in tasks:
                i.join()
            if None in task_:
                log.log("任务队列已空！","info")
                break
if __name__ == '__main__':
    a = YX_Spider()
    a.start_req()
    a.run(CON_NUMS)
