from req import Aio_Req,Sin_Req
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
class YX_Spider(object):
    def __init__(self):
        self.cars = task.tasks
        self.base_url = "https://www.xin.com/"
        self.base_report = "https://www.xin.com/apis/ajax_report/get_chake_report/?carid="
    def start_req(self):
        r = requests.get("https://www.xin.com/apis/Ajax_common/get_home_city/?cityid=201")
        data = json.loads(r.text)
        for i in data["data"]["city_all"]:
            city = data["data"]["city_all"][i]["ename"]
            city_name =data["data"]["city_all"][i]["cityname"]
            for i in self.cars:
                start_link = urljoin(self.base_url,city+r'/'+i)
                log.log(start_link,"debug")
                task_queue.add_task(Sin_Req(start_link,callback=self.parse_items,meta = {"city_name":city_name}))
    def parse_items(self,response):
        html = etree.HTML(response["response"])
        city_name = response["city_name"]
        items = html.xpath('//li[@class="con caritem conHeight"]')
        next_item = html.xpath('//div[@class="con-page search_page_link"]/a')
        log.log("下一页条目   "+str(next_item),"debug")
        for j in items:
            data = dict()
            title = j.xpath('@data-title')
            car_id = j.xpath('@data-carid')
            price = j.xpath('@data-price')
            link = j.xpath('div[@class="across"]/a/@href')
            city_id = j.xpath('div[@class="across"]/a/@data-cityid')
            brand_id = j.xpath('div[@class="across"]/a/@data-brandid')
            seriesid = j.xpath('div[@class="across"]/a/@data-seriesid')
            year_age = j.xpath('div[@class="across"]/div[@class="pad"]/span[1]/text()')
            data["title"] = title
            data["car_id"] = car_id
            data["price"] = price
            data["link"] = link
            data["city_id"] = city_id
            data["city_name"] = city_name
            data["brand_id"] = brand_id
            data["series_id"] = seriesid
            data["year"] = year_age[0]
            data["age"] = year_age[1]
            log.log(str(data),"info")
            mon.insert("item_data",data)
            if link:
                if car_id:
                    report_task = Sin_Req(self.base_report+car_id[0],self.parse_report,meta = {"car_id":car_id})
                    report_task.headers["Referer"] = urljoin(self.base_url,link[0])
                    task_queue.add_task(report_task)
        if next_item:
            next_page = next_item[-1].xpath('text()')
            if next_page:
                if "下一页" in next_page[0]:
                    next_link = next_item[-1].xpath('@href')[0]
                    log.log("下一页   "+next_link,"debug")
                    task_queue.add_task(Sin_Req(urljoin(self.base_url,next_link),callback=self.parse_items,meta = {"city_name":city_name}))
    def parse_report(self,response):
        log.log("检测报告","debug")
        car_id = response["car_id"]
        raw_data = response["response"].encode("utf-8").decode("unicode_escape")
        report_data = json.loads(raw_data)
        data = {}
        data[car_id[0]] = report_data
        log.log("report data   "+str(data),"info")
        mon.insert("report_data",data)
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
    a = YX_Spider()
    # a.start_req()
    a.run(CON_NUMS)
