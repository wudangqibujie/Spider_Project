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
import task
from urllib.parse import urljoin
from db import Mon
task_queue = TaskQueue()
mon = Mon()
class QCZJ_Spider(object):
    def __init__(self):
        self.cars = task.tasks
        self.key_link = "https://club.api.autohome.com.cn/web/topicdetail/rv?fun=jsonprv&ids={ids}&callback=jsonprv&_={time_}&callback=jsonprv"
    def start_req(self):
        """
        初始化每个车型的首页论坛页面
        :return:
        """
        for i in self.cars.keys():
            page = 1
            car = i
            base_link = self.cars[i]
            task_queue.add_task(Aio_Req(base_link.format(page),self.parse_items,meta={"page":page,"base_link":base_link,"car":i}))
    def parse_items(self,response):
        """
        :param response:返回帖子列表页面数据
        :return: 构造评论数和点击数的数据请求
        """
        text = response["response"]
        page = response["page"]
        base_link = response["base_link"]
        log.log(base_link,"debug")
        car = response["car"]
        try:
            if text.strip():
                id_ = re.findall(r'data-topicid="(.*?)">', text, re.S)
                link = re.findall(r' <a href="(.*?)" >', text, re.S)
                title = re.findall(r'<h4>(.*?)</h4>', text, re.S)
                comm = re.findall(r'ass="comment">(.*?)帖</span>', text, re.S)
                time_ = re.findall(r'<time>(.*?)</time>', text, re.S)
                id_lst = []
                for i in range(len(id_)):
                    data = dict()
                    data["topic_id"] = id_[i]
                    id_lst.append(id_[i])
                    data["car"] = car
                    data["link"] = link[i]
                    data["title"] = title[i].strip()
                    data["comm"] = comm[i]
                    data["time"] = time_[i]
                    log.log(str(data),"info")
                    mon.insert("item_data",data)
                if id_lst:
                    print(id_lst)
                    ids = "%2C".join(id_lst)
                    log.log(ids,"debug")
                    time_ = int(time.time()*1000)
                    comm_view_link = self.key_link.format(ids = ids,time_=time_)
                    log.log(comm_view_link,"debug")
                    task_queue.add_task(Aio_Req(comm_view_link,callback=self.parse_comment_view))
                task_queue.add_task(Aio_Req(base_link.format(page+1),self.parse_items,meta={"page":page+1,"base_link":base_link,"car":car}))
        except Exception as e:
            log.log(str(e),"error")
            log.log(base_link+str(page),"error")
            log.log(text,"error")
    def parse_comment_view(self,response):
        """
        解析出评论数和点击数
        :param response:
        :return:
        """
        try:
            raw_data = re.findall('jsonprv'+'\('+'(.*?)'+ '\)'+'$',response["response"])
            if raw_data:
                data = eval(raw_data[0])
                for i in data:
                    mon.insert("comm_view",i)
                    log.log(str(i),"info")
        except Exception as e:
            log.log(str(e),"error")
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
    a = QCZJ_Spider()
    a.start_req()
    a.run(CON_NUMS)
