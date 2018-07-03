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
        self.start_link = "http://db.m.auto.sohu.com/brand?referid=101home00020001"#车型目录页
    def start_req(self):
        a = Aio_Req(self.start_link,self.parse_brand)
        loop = asyncio.get_event_loop()
        tasks = [a.aio_req()]
        loop.run_until_complete(asyncio.wait(tasks))
    def parse_brand(self,response):
        """
        :param response: 返回品牌条目页的
        :return:构造车系的请求
        """
        html = etree.HTML(response["response"])
        items = html.xpath('//div[@class="img_list_bg"]/ul/li')
        for i in items:
            data = {}
            name = i.xpath('h4/a/text()')[0]
            link = urljoin(self.host,i.xpath('h4/a/@href')[0])
            brand_id = i.xpath('a/@class')[0]
            data["brand_name"] = name
            data["brand_link"] = link
            data["brand_id"] = brand_id
            log.log(str(data),"info")
            task_queue.add_task(Aio_Req(link,self.parse_series,meta={"brand":name}))
            mon.insert("brand_info",data)
    def parse_series(self,response):
        """
        :param response:请求到的车系页面
        :return:构造车型的口碑请求
        """
        brand = response["brand"]
        html = etree.HTML(response["response"])
        items = html.xpath('//ul[@class="pt_list"]/li')
        for i in items:
            data = {}
            series_name = i.xpath('a/div[@class="info"]/strong/text()')
            series_link = urljoin(self.host,i.xpath('a/@href')[0])
            data["series_name"] = series_name
            data["series_link"] = series_link
            data["brand"] = brand
            log.log(str(data),"info")
            kb_link = re.sub(r'(\?param=.*?)$','dianping.shtml',series_link)
            task_queue.add_task(Aio_Req(kb_link,self.parse_kb,meta={"brand":brand,"series":series_name}))
            mon.insert("series_info",data)
    def parse_kb(self,response):
        """
        :param response:请求成功的口碑页面
        :return: 解析出口碑数据持久化至数据库
        """
        brand = response["brand"]
        series = response["series"]
        html = etree.HTML(response["response"])
        star_num = html.xpath('//span[@class="starnum"]/strong/text()')
        fuel = html.xpath('//div[@class="r_part"]/h4[3]/text()')
        item_star = html.xpath('//ul[@class="dpbox"]/li')
        selec_link = html.xpath('//nav[@class="topnav"]/ul/li')
        sele_data = {}
        for j in selec_link:
            sele_name = j.xpath('a/text()')[0].strip() if j.xpath('a/text()') else "NO"
            sele_link = urljoin(self.host,j.xpath('a/@href')[0]) if  j.xpath('a/@href') else "NO_link"
            sele_data[sele_name] = sele_link
        item_data = {}
        for i in item_star:
            item_name = i.xpath('text()')[0]
            item_star = i.xpath('a/span/@style')
            item_data[item_name] = item_star
        data = {}
        data["brand"] = brand
        data["series"] = series
        data["star"] = star_num
        data["fuel"] = fuel
        data["score_info"] = item_data
        data["sele_info"] = sele_data
        print(data)
        mon.insert("kb",data)
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
