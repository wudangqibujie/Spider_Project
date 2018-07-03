from req import Aio_Req,Sin_Req
from lxml import etree
import asyncio
from settings import *
import time
import threading as th
from m_queue import TaskQueue
import requests
import re
import json
from log import log
from urllib.parse import urljoin
from db import Mon
task_queue = TaskQueue()
mon = Mon()
class SH_Spider(object):
    def __init__(self):
        self.host = "http://db.m.auto.sohu.com/"
        self.base_link = "http://db.m.auto.sohu.com/model_1992/dianping/list-more.json?number=5&page={}&jsonpCallback=article&_=1528591590986&callback=article"
    def start_req(self):
        for i in mon.data_find("kb"):
            if "口碑" in i["sele_info"]:
                brand = i["brand"]
                series = i["series"][0].strip()
                kb_link = i["sele_info"]["口碑"].replace('.shtml',"/list-more.json?number=5&page={}&jsonpCallback=article&_=1528591590986&callback=article")
                task_queue.add_task(Aio_Req(kb_link.format(1),self.parse_kb_detail,meta={"base_link":kb_link,"brand":brand,"series":series,"page":1}))
    def parse_kb_detail(self,response):
        brand = response["brand"]
        series = response["series"]
        page = response["page"]
        base_link = response["base_link"]
        text = response["response"]
        try:
            if len(text) > 50:
                data = {}
                data["brand"] = brand
                data["series"] = series
                data["kb_raw"] = text
                log.log(str(data),"info")
                mon.insert("kb_detail",data)
                task_queue.add_task(Aio_Req(base_link.format(page+1),self.parse_kb_detail,meta={"base_link":base_link,"brand":brand,"series":series,"page":page+1}))
        except:
            log.log(brand+series+base_link+str(page),"error")
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
    a = SH_Spider()
    a.start_req()
    a.run(CON_NUMS)
