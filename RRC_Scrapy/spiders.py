from req import Aio_Req,Sin_Req
from lxml import etree
import asyncio
from settings import *
import threading as th
from m_queue import TaskQueue
from log import log
import task
from urllib.parse import urljoin
from urllib.parse import urlsplit
from db import Mon
task_queue = TaskQueue()
mon = Mon()
class RRC_Spider(object):
    def __init__(self):
        self.start_urls = task.tasks
        self.base_url = "https://www.renrenche.com/"
    def start_req(self):
        for i in self.start_urls:
            start_page = 1
            task_queue.add_task(Sin_Req(i+"p"+str(start_page)+r"/",callback=self.parse_item,meta={"now_page":start_page,"base_link":i}))
    def parse_item(self,response):
        """
        :param response:列表页的响应
        :return: 构造详情页的检测报告请求
        """
        html = etree.HTML(response["response"])
        items = html.xpath('//ul[@class="row-fluid list-row js-car-list"]/li')
        log.log(str(items), "debug")
        if items:
            for i in items:
                data = dict()
                link = i.xpath('a/@href')
                car_id = i.xpath('a/@data-car-id')
                title = i.xpath('div[@class="schedule btn-base btn-wireframe"]/@data-title')
                city = i.xpath('a/div[@class="img-backgound"]/div[@class="position-bg"]/span/text()')
                year_age = i.xpath('a/div[@class="mileage"]/span[1]/text()')
                price = i.xpath('a/div[@class="tags-box"]/div[@class="price"]/text()')
                data["car_id"] = car_id
                data["title"] = title
                data["link"] = link
                data["city"] = city
                data["year_age"] = year_age
                data["price"] = price
                log.log(str(data),"info")
                mon.insert("data",data)
                if link:
                    detail_link = urljoin(self.base_url,link[0])
                    task_queue.add_task(Sin_Req(detail_link,callback=self.parse_detail,meta={"data_id":car_id}))
                    log.log("detail_link   "+detail_link,"debug")
            base_link = response["base_link"]
            next_page = response["now_page"] + 1
            next_link = base_link+"p"+str(next_page)+r"/"
            log.log(next_link,"debug")
            task_queue.add_task(Sin_Req(next_link,callback=self.parse_item,meta={"base_link":base_link,"now_page":next_page}))
    def parse_detail(self,response):
        """
        解析检测报告详情页
        :param response:
        :return:
        """
        car_id = response["data_id"]
        html = etree.HTML(response["response"])
        items = html.xpath('//div[@class="other clearfixnew"]/div')
        for i in items:
            for j in i.xpath('div[@class="option"]'):
                data = dict()
                data["car_id"] = car_id
                option_name = j.xpath('div[@class="child-title"]/text()')
                option_counts = j.xpath('div[@class="mun"]/text()')
                data["option_name"] = option_name
                data["option_counts"] = option_counts
                if j.xpath('a[@class="test-fail-box"]'):
                    fetal_counts = j.xpath('a[@class="test-fail-box"]/div[@class="test-fail"]/div[@class="mun"]/text()')
                    data["fetal_counts"] = fetal_counts
                else:
                    fetal_counts = 0
                    data["fetal_counts"] = fetal_counts
                mon.insert("report_data",data)
                log.log(str(data),"info")
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
    a = RRC_Spider()
    a.start_req()
    a.run(CON_NUMS)
