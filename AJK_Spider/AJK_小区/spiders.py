from req import Aio_Req,Sin_Req
from lxml import etree
import re
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
class Ajk_Xq_Spider(object):
    def __init__(self):
        self.task = task.tasks
        self.base_comm_link = "https://zhengzhou.anjuke.com/v3/ajax/prop/pricetrend/?commid="
    def start_req(self):
        """
        把种子url初始化封装成Request放入带抓取任务队列
        :return: 初始化Request对象
        """
        for k in self.task.keys():
            city = k
            link = self.task[city]
            task_queue.add_task(Sin_Req(link+r'community/',self.parse_items,meta={"city":city}))
    def parse_items(self,response):
        """
        解析所需数据字段和下一页连接
        :param response: 列表页请求成功返回的数据内容
        :return: 下一页链接，重新封装成Request放入任务队列，数据字段持久化至MongoDB,封装成详情页的价格数据请求Request对象进任务队列内
        """
        html = etree.HTML(response["response"])
        city = response["city"]
        item_data = html.xpath('//div[@_soj="xqlb"]')
        next_item = html.xpath('//div[@class="multi-page"]/a')
        if next_item:
            if "下一页" in next_item[-1].xpath('text()')[0]:
                next_url = next_item[-1].xpath('@href')
                if next_url:
                    log.log("下一页链接   "+next_url[0],"debug")
                    next_task =Sin_Req(next_url[0],self.parse_items,meta={"city":city})
                    task_queue.add_task(next_task)
        if item_data:
            for i in item_data:
                item = dict()
                item["city"] = city
                item["title"] = i.xpath('a/@title')
                item["link"] = i.xpath('a/@href')
                item["address"] = i.xpath('div[@class="li-info"]/address/text()')
                item["year"] = i.xpath('div[@class="li-info"]/p[@class="date"]/text()')
                item["price"] = i.xpath('div[@class="li-side"]/p[1]/strong/text()')
                if item["link"]:
                    commid = re.findall(r'view/(.*?)$',item["link"][0])
                    if commid:
                        comm_link = self.base_comm_link+commid[0]
                        task_queue.add_task(Sin_Req(comm_link,self.parse_comm_trend,meta={"commid":commid}))
                log.log(str(item),"info")
                mon.insert("ajk_xiaoqu",item)
    def parse_comm_trend(self,response):
        """
        :param response:返回得到价格趋势数据
        :return: 持久化到数据库
        """
        commid = response["response"]
        try:
            data = json.loads(response["response"])
            data["commid"] = commid
            mon.insert("price_trend",data)
            log.log(str(data),"info")
        except Exception as e:
            log.log(commid)
            log.log(str(e),"error")
    def run(self,nums):
        """
        :param nums:并发数
        :return:
        """
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
    a = Ajk_Xq_Spider()
    a.start_req()
    a.run(CON_NUMS)
