from req import Aio_Req,Sin_Req
from lxml import etree
import asyncio
from settings import *
import threading as th
from m_queue import TaskQueue
import requests
import json
from selenium import webdriver
from log import log
from urllib.parse import urljoin
from db import Mon
task_queue = TaskQueue()
mon = Mon()
class BIN_Spider(object):
    def __init__(self):
        self.follow_base_link = "https://www.zhihu.com/api/v4/columns/hemingke/followers?include=data%5B%2A%5D.follower_count%2Cgender%2Cis_followed%2Cis_following&limit=10&offset={}"
    def start_req(self):
        for i in range(17069):
            task_queue.add_task(Aio_Req(self.follow_base_link.format(i*10),self.parse_follow_lst,meta={"offset":i}))
    def parse_follow_lst(self,response):
        offset = response["offset"]
        try:
            data = json.loads(response["response"])
            mon.insert("follow_lst",data)
            for i in data["data"]:
                log.log(str(i),"info")
                mon.insert("follower",i)
        except Exception as e:
            log.log(str(e),"error")
            log.log(str(offset),"error")
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
    a = BIN_Spider()
    a.start_req()
    a.run(CON_NUMS)
