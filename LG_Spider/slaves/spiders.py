from req import Aio_Req,Sin_Req,Post_Req
from lxml import etree
import asyncio
from settings import *
import urllib.parse
import threading as th
import re
from m_queue import TaskQueue
import requests
import json
from log import log
import task
from urllib.parse import urljoin
from db import Mon
task_queue = TaskQueue()
mon = Mon()
class LG_Spider(object):
    def __init__(self):
        self.poses = task.poses
        self.cities = task.cities
        self.base_url = "https://www.lagou.com/jobs/positionAjax.json"
    def start_req(self):
        for c in self.cities:
            for p in self.poses:
                page = 1
                url_data = {"px": "default", "city": c, "needAddtionalResult": "false"}
                post_data = {"first": "false", "pn": 1, "kd": p}
                add_headers = 'https://www.lagou.com/jobs/list_'+urllib.parse.quote(p)+'?px=default&city='+urllib.parse.quote(c)
                task = Post_Req(self.base_url,post_data,url_data,callback=self.parse_max_page,meta={"post_data":post_data,"url_data":url_data})
                task.headers["Referer"] = add_headers
                task_queue.add_task(task)
    def parse_max_page(self,response):
        first_data = response["response"]
        post_data = response["post_data"]
        data = dict()
        data["data"] = first_data
        url_data = response["url_data"]
        log.log("first data  "+str(first_data),"info")
        mon.insert("data",data)
        try:
            total = int(re.findall(r'totalCount":(.*?),', first_data)[0])
            log.log("最大页数  "+str(total),"debug")
            log.log("最大数量  "+str(total),"debug")
            for page in range(1, int(total / 15) + 2):
                post_data["pn"] = page
                task = Post_Req(self.base_url,post_data,url_data,callback=self.parse_data)
                add_headers = 'https://www.lagou.com/jobs/list_' + urllib.parse.quote(post_data["kd"]) + '?px=default&city=' + urllib.parse.quote(url_data["city"])
                task.headers["Referer"] = add_headers
                task_queue.add_task(task)
        except Exception as e:
            log.log(str(post_data)+"  "+str(url_data)+"  "+str(e),"error")
    def parse_data(self,response):
        data = response["response"]
        log.log(data,"info")
        da = dict()
        mon.insert("data",da)
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
    a = LG_Spider()
    # a.start_req()
    a.run(CON_NUMS)
