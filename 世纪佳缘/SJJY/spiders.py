from req import Aio_Req,Sin_Req,Post_Req
from lxml import etree
import asyncio
import json
import re
from settings import *
import threading as th
from m_queue import TaskQueue
from log import log
from urllib.parse import urljoin
from db import Mon
task_queue = TaskQueue()
mon = Mon()
class SJJY_Spider(object):
    def __init__(self):
        self.start_urls = "http://search.jiayuan.com/v2/search_v2.php"
    def start_req(self):
        """
        构造post参数进行请求
        :return:
        """
        for i in range(1,40000):
            for j in ["m","f"]:
                post_base_data = {
                    'sex': j,
                    'stc': '23:1',
                    'sn': 'default',
                    'sv': '1',
                    'p': i,
                    'listStyle': 'bigPhoto',
                    'pri_uid': '0',
                    'jsversion': 'v5'
                }
                task_queue.add_task(Post_Req(self.start_urls,post_data=post_base_data,callback=self.parse_data,meta={"post_data":{j:i}}))
    def parse_data(self,response):
        """
        解析所需数据
        :param response:
        :return:
        """
        post_data = response["post_data"]
        try:
            text = response["response"].encode("utf-8").decode("unicode_escape")
            text_1 = re.findall(r'"userInfo":(.*?]),"second_searc', text)[0]
            text_first = json.loads(text_1)
            text_2 = re.findall(r'express_search":(.*?),"cond', text)[0]
            text_second = json.loads(text_2)
            log.log(str(text_second),"debug")
            log.log(str(text_first),"debug")
            for i in text_first:
                log.log(str(i),"info")
                mon.insert("data",i)
            for j in text_second:
                log.log(str(j),"info")
                mon.insert("data",j)
        except:
            log.log(str(post_data)+"\n","error")
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
    a = SJJY_Spider()
    a.start_req()
    a.run(CON_NUMS)
