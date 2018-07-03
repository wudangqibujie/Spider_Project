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
        self.base_link = "https://api.zhihu.com/people/{}"
    def start_req(self):
        detail_lst = set()
        after = set()
        for i in mon.data_find("follower"):
            detail_lst.add(i["id"])
        for d in mon.data_find("user_detail"):
            if "id " in d:
                after.add(d["id"])
        print(len(list(detail_lst-after)))
    def parse_detail(self,response):
        uid = response["uid"]
        try:
            data = json.loads(response["response"])
            log.log(str(data),"info")
            mon.insert("user_detail",data)
        except Exception as e:
            log.log(str(e),"error")
            log.log(uid)
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

