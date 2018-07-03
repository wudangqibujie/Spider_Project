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
class BIN_Spider(object):
    def __init__(self):
        self.first_req = "https://www.zhihu.com/api/v4/columns/hemingke/articles?include=data%5B*%5D.admin_closed_comment%2Ccomment_count%2Csuggest_edit%2Cis_title_image_full_screen%2Ccan_comment%2Cupvoted_followees%2Ccan_open_tipjar%2Ccan_tip%2Cvoteup_count%2Cvoting%2Ctopics%2Creview_info%2Cauthor.is_following"
        self.arti_req = "https://www.zhihu.com/api/v4/columns/hemingke/articles?include=data%5B%2A%5D.admin_closed_comment%2Ccomment_count%2Csuggest_edit%2Cis_title_image_full_screen%2Ccan_comment%2Cupvoted_followees%2Ccan_open_tipjar%2Ccan_tip%2Cvoteup_count%2Cvoting%2Ctopics%2Creview_info%2Cauthor.is_following&limit=10&offset={offset}"
        self.comm_req = "https://www.zhihu.com/api/v4/articles/{comm_id}/comments?include=data%5B*%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author&order=normal&limit=20&offset={offset}&status=open"
    def start_req(self):
        """
        数据冰山发布的文章列表抓取
        :return:
        """
        task_queue.add_task(Aio_Req(self.first_req,self.parse_arti_lst))
        for i in range(1,19):
            task_queue.add_task(Aio_Req(self.arti_req.format(offset=i*10),self.parse_arti_lst))
    def parse_arti_lst(self,response):
        """
        返回的Json数据解析
        :param response:返回的文章数据
        :return:构造对应文章的评论的Url，构造成Request放入任务队列
        """
        try:
            data = json.loads(response["response"])
            log.log(str(data),"info")
            for i in data["data"]:
                log.log(str(i),"info")
                comm_id = i["id"]
                offset = 0
                task_queue.add_task(Aio_Req(self.comm_req.format(comm_id=comm_id,offset=offset),self.parse_comm,meta = {"comm_id":comm_id,"offset":offset}))
        except Exception as e:
            log.log(str(e),"error")
    def parse_comm(self,response):
        """
        :param response:文章的评论数据
        :return: 把数据持久化进数据库并把下一页的评论数据请求放入任务队列
        """
        offset = response["offset"]
        comm_id = response["comm_id"]
        try:
            text = json.loads(response["response"])
            data={}
            data["comm_id"] = comm_id
            data["arti_data"] = text
            log.log("评论    "+str(data),"info")
            mon.insert("comm_lst",data)
            if not text["paging"]["is_end"]:
                log.log("下一个    ","debug")
                next_task = Aio_Req(self.comm_req.format(comm_id=comm_id,offset=20*(offset+1)),self.parse_comm,meta={"comm_id":comm_id,"offset":offset})
                task_queue.add_task(next_task)
        except Exception as e:
            log.log(str(e),"error")
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
    a = BIN_Spider()
    a.start_req()
    a.run(CON_NUMS)
