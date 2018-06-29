from req import Aio_Req,Sin_Req
from lxml import etree
import asyncio
from settings import *
import threading as th
from m_queue import TaskQueue
from log import log
from urllib.parse import urljoin
from db import Mon
task_queue = TaskQueue()
mon = Mon()
class QF_Spider(object):
    def __init__(self):
        self.start_urls = "https://beijing.qfang.com/sale"
    def start_req(self):
        s = Sin_Req(self.start_urls,self.parse_start)
        s.get()
    def parse_start(self,response):
        html = etree.HTML(response["response"])
        items = html.xpath('//ul[@class="cities-opts clearfix"]/li')
        log.log(str(items), "debug")
        for i in items:
            a_items = i.xpath('p/a[@class="highlight"]')
            log.log(str(a_items), "debug")
            if a_items:
                for j in a_items:
                    data = dict()
                    name = j.xpath('text()')[0]
                    link = j.xpath('@href')[0]
                    data["city_name"] = name
                    data["city_link"] = link
                    mon.insert("city_data",data)
                    log.log(str(data)+"  ","info")
                    task_queue.add_task(Sin_Req(url="https:"+link,callback=self.parse_zones,meta={"city_link":link,"city_name":name}))
    def parse_zones(self,response):
        city_name = response["city_name"]
        base_link = response["city_link"]
        html = etree.HTML(response["response"])
        items = html.xpath('//ul[@class="search-area-detail clearfix"]/li')[1:]
        log.log("ZONE   "+str(items),"debug")
        for i in items:
            zone_ = i.xpath('a/text()')
            link_ = i.xpath('a/@href')
            if zone_:
                data = {}
                data["zone_name"] = zone_[0]
                data["zone_link"] = link_[0]
                log.log(str(data),"info")
                task_queue.add_task(Sin_Req("https:"+urljoin(base_link,link_[0]),self.parse_details,meta={"city_name":city_name,"zone_name":zone_[0],"zone_base_url":"https:"+urljoin(base_link,link_[0])}))
    def parse_details(self,response):
        city_name = response["city_name"]
        zone_name = response["zone_name"]
        html = etree.HTML(response["response"])
        items = html.xpath('//div[@class="house-detail"]/ul/li')
        next_items = html.xpath('//div[@class="pages-box clearfix"]/div[2]/a[@class="turnpage_next"]')
        if next_items:
            if "下一页" in next_items[0].xpath('span/text()')[0]:
                next_page = next_items[0].xpath('@href')
                log.log(str(next_page),"debug")
                if next_page:
                    zone_base_url = response["zone_base_url"]
                    next_link = urljoin(zone_base_url,next_page[0])
                    log.log(next_link,"info")
                    task_queue.add_task(Sin_Req(next_link,self.parse_details,meta={"city_name":city_name,"zone_name":zone_name,"zone_base_url":zone_base_url}))
        if items:
            for i in items:
                data = {}
                title = i.xpath('div[1]/p[@class="house-title"]/a/@title')
                link = i.xpath('a/@href')
                base_info = i.xpath('div[1]/p[@class="house-about clearfix"]/span/text()')
                address = i.xpath('div[1]/p[@class="house-address clearfix"]/span[@class="whole-line"]/a/text()')
                price = i.xpath('div[@class="show-price"]/span[@class="sale-price"]/text()')
                uni_price = i.xpath('div[@class="show-price"]/p/text()')
                data["title"] = title
                data["link"] = link
                data["base_info"] = base_info
                data["address"] = address
                data["price"] = price
                data["uni_price"] = uni_price
                log.log(str(data),"info")
                mon.insert("data",data)
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
    a = QF_Spider()
    a.start_req()
    a.run(CON_NUMS)
