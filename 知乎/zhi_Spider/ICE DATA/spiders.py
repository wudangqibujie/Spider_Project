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
        self.base_url = "https://www.zhihu.com/api/v4/members/he-ming-ke/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={}&limit=20"
        self.add_headers = {
            'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
            'referer': 'https://www.zhihu.com/org/shu-ju-bing-shan/activities',
            }
        self.base_user_url = "https://api.zhihu.com/people/{u_id}"
    def start_req(self):
        """
        用户关注列表的数据抓取
        :return:
        """
        offset = 0
        task = Sin_Req(self.base_url.format(offset*10),callback = self.parse_follow_lst,meta={"offset":offset})
        task.headers.update(self.add_headers)
        task_queue.add_task(task)
    def parse_follow_lst(self,response):
        """
        :param response: 关注用户的数据
        :return:构造详细关注用户信息的请求任务
        """
        offset = response["offset"]
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
        """
        解析用户的详细信息持久化到数据库
        :param response:
        :return:
        """
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
    a.start_req()
    a.run(CON_NUMS)
