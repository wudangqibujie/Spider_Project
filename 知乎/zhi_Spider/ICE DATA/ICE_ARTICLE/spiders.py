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
class ICE_Article_Spider(object):
    def __init__(self):
        self.first_req = "https://www.zhihu.com/org/shu-ju-bing-shan/activities"
        self.article_start_url = "https://www.zhihu.com/api/v4/members/shu-ju-bing-shan/activities?limit=7&after_id=1522120267&desktop=True"
        self.comment_base_url = "https://www.zhihu.com/api/v4/articles/{id}/comments?include=data%5B*%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author&order=normal&limit=20&offset={page}&status=open"
    def article_first_req(self):
        """
        首页前几条的文章列表的抓取
        :return:
        """
        browser = webdriver.PhantomJS()
        browser.get(self.first_req)
        html = etree.HTML(browser.page_source)
        self.get_start_data(html)
    def get_start_data(self,html):
        """
        首页的网页解析
        :param html:
        :return:
        """
        items = html.xpath('//div[@class="List-item"]')
        for i in items:
            data = dict()
            action = i.xpath('div[@class="List-itemMeta"]/div[@class="ActivityItem-meta"]/span[1]/text()')[0]
            title = i.xpath('div[@class="ContentItem ArticleItem"]/h2[1]/a/text()')[0]
            link = i.xpath('div[@class="ContentItem ArticleItem"]/@data-zop')[0]
            like_count = i.xpath('div[@class="ContentItem ArticleItem"]/div[@class="ContentItem-meta"]/div[@class="ArticleItem-extraInfo"]/span/button/text()')[0]
            comment_count = i.xpath('div[@class="ContentItem ArticleItem"]/div[@class="RichContent is-collapsed"]/div[@class="ContentItem-actions"]/button[2]/text()')[0]
            abstract = i.xpath('div[@class="ContentItem ArticleItem"]/div[@class="RichContent is-collapsed"]/div[2]/span/text()')
            data["title"] = title
            data["action"] = action
            data["link"] = link
            data["like_count"] = like_count
            data["comment_count"] = comment_count
            data["abstract"] = abstract
            log.log(str(data),"info")
            # mon.insert("start_data",data)
    def article_start_req(self):
        """
        构造动态加载的文章列表数据请求
        :return:
        """
        add_headers = {
            'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
            'referer': 'https://www.zhihu.com/org/shu-ju-bing-shan/activities'
        }
        s = Sin_Req(self.article_start_url,callback=self.parse_arti_data,meta={"add_headers":add_headers})
        s.headers.update(add_headers)
        task_queue.add_task(s)
    def parse_arti_data(self,response):
        """
        解析所发布的文章数据，并构造文章的评论的请求
        :param response:
        :return:
        """
        data = json.loads(response["response"])
        add_headers = response["add_headers"]
        if 'paging' in data:
            if not data["paging"]["is_end"]:
                print(data)
                for i in data["data"]:
                    log.log(str(i),"info")
                    # mon.insert("data",data)
                    if i["target"]:
                        if  i["target"]["id"]:
                            article_id = i["target"]["id"]
                            page = 0
                            comm_task = Sin_Req(self.comment_base_url.format(id = article_id,page = 20*page),callback=self.parse_comment,meta={"add_headers":add_headers,"page":page,"article_id":article_id})
                            comm_task.headers.update(add_headers)
                            # print(comm_task.headers)
                            task_queue.add_task(comm_task)
                next_link = data["paging"]["next"]
                log.log("下一个文章链接   "+ next_link,"debug")
                s = Sin_Req(next_link,callback=self.parse_arti_data,meta={"add_headers":add_headers})
                s.headers.update(add_headers)
                print(s.headers)
                task_queue.add_task(s)
            else:
                for i in data["data"]:
                    log.log(str(i),"info")
                    mon.insert("data",data)
    def parse_comment(self,response):
        """
        解析每个文章的评论内容
        :param response:
        :return:
        """
        page = response["page"]
        article_id = response["article_id"]
        add_headers = response["add_headers"]
        try:
            data = json.loads(response["response"])
            if "paging" in data:
                if not data["paging"]["is_end"]:
                    log.log(str(data),"info")
                    mon.insert("comment_data",data)
                    next_comment_task = Sin_Req(self.comment_base_url.format(id = article_id,page = 20*(page+1)),callback=self.parse_comment,meta={"add_headers":add_headers,"page":page+1,"article_id":article_id})
                    next_comment_task.headers.update(add_headers)
                    task_queue.add_task(next_comment_task)
                else:
                    log.log("Last Comment Data"+str(data),"info")
                    mon.insert("comment_data",data)
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
    a = ICE_Article_Spider()
    # a.article_first_req()
    a.article_start_req()
    a.run(CON_NUMS)
