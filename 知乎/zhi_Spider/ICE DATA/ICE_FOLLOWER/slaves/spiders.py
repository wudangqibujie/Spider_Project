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
class ICE_Follower_Spider(object):
    def __init__(self):
        self.base_url = "https://www.zhihu.com/api/v4/columns/hemingke/followers?include=data%5B%2A%5D.follower_count%2Cgender%2Cis_followed%2Cis_following&limit=10&offset={}"
        self.add_headers = {
            'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
            'referer': 'https://www.zhihu.com/org/shu-ju-bing-shan/activities',
            }
        self.base_user_url = "https://api.zhihu.com/people/{u_id}"
    def start_req(self):
        offset = 0
        task = Sin_Req(self.base_url.format(offset*10),callback = self.parse_follow_lst,meta={"offset":offset})
        task.headers.update(self.add_headers)
        task_queue.add_task(task)

    def parse_follow_lst(self,response):
        offset = response["offset"]
        print(offset)
        try:
            data = json.loads(response["response"])
            log.log(str(data),"info")
            mon.insert("follower_lst",data)
            if data["data"]:
                print("BMW")
                for j in data["data"]:
                    user_id = j["id"]
                    log.log(str(j),"info")
                    log.log(str(user_id),"debug")
                    detal_task = Sin_Req(self.base_user_url.format(u_id = user_id),callback=self.parse_user_detail)
                    detal_task.headers.update(self.add_headers)
                    task_queue.add_task(detal_task)
            if data["paging"]:
                if not data["paging"]["is_end"]:
                    next_task = Sin_Req(self.base_url.format(10*(offset+1)),self.parse_follow_lst,meta = {"offset":offset+1})
                    next_task.headers.update(self.add_headers)
                    task_queue.add_task(next_task)
        except:
            log.log(str(offset),"error")
    def parse_user_detail(self,response):
        try:
            data = json.loads(response["response"])
            mon.insert("user_detail",data)
            log.log(str(data),"info")
        except Exception as e:
            log.log(str(e),"error")
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
    a = ICE_Follower_Spider()
    a.run(CON_NUMS)
