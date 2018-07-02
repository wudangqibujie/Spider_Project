from req import Aio_Req,Sin_Req,Post_Req
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
class GZ_Spider(object):
    def __init__(self):
        self.cars = task.tasks
        self.car_brand_get = "https://m.guazi.com/sz/buy/?act=getTagByMinor"
        self.base_items_link = "https://m.guazi.com/www/{series}/o{page}/?act=getNext"
    def car_req(self):
        """
        汽车品牌基本信息抓取
        :return:
        """
        for k in self.cars.keys():
            post_data = {"minorId":self.cars[k]}
            # log.log(str(post_data),"debug")
            s = Post_Req(self.car_brand_get,post_data,self.parse_brand)
            task_queue.add_task(s)
    def parse_brand(self,response):
        """
        解析得到汽车品牌的基本信息
        :param response:
        :return:
        """
        try:
            data = json.loads(response["response"])
            for i in data["data"]["option"]:
                log.log(str(i),"info")
                mon.insert("car_info",i)
                car_name = i["text"]
                page = 1
                task_link = self.base_items_link.format(series = i["tag_url"],page=page)
                # log.log(task_link,"debug")
                item_task = Sin_Req(task_link,self.parse_item,meta={"cur_link":task_link,"car_name":car_name,"page":page,"series":i["tag_url"]})
                task_queue.add_task(item_task)
        except Exception as e:
            log.log(str(e),"error")
    def parse_item(self,response):
        """
        二手车列表页的抓取
        :param response:
        :return:
        """
        page = response["page"]
        cur_link = response["cur_link"]
        series = response["series"]
        car_name = response["car_name"]
        try:
            req_data = json.loads(response["response"])
            if req_data["data"]["thisCity"]:
                data = dict()
                data["car_name"] = car_name
                data["item_info"] = req_data["data"]["thisCity"]
                task_queue.old_task(cur_link)
                log.log(str(data),"info")
                mon.insert("item_data",data)
                next_link = self.base_items_link.format(series = series,page = page+1)
                log.log("下一页连接    "+next_link,"debug")
                next_task = Sin_Req(next_link,self.parse_item,meta={"cur_link":cur_link,"car_name":car_name,"page":page,"series":series})
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
    a = GZ_Spider()
    # a.city_req()
    a.car_req()
    a.run(CON_NUMS)
