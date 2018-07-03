import aiohttp
import requests
import redis
import asyncio
from settings import *
from requests import Request
from lxml import etree
import pickle
from m_queue import TaskQueue
import random
from log import log
tt = TaskQueue()
class Aio_Req(object):
    def __init__(self,url,callback,meta = {}):
        """
        :param url:带抓取链接
        :param callback: 回调函数
        :param meta: 需要函数间传递的参数
        """
        self.url = url
        self.callback = callback
        self.meta = meta
        self.headers = {"User-Agent":random.choice(agents)}
    async def aio_req(self):
        async with aiohttp.ClientSession() as resp:
            try:
                async with resp.get(url=self.url,headers=self.headers) as resp:
                    page = await resp.text()
                    self.meta["response"] = page
                    log.log(str(resp.status) + "   " + self.url, "info")
                    self.callback(self.meta)
                    tt.old_task(self.url)
            except Exception as e:
                print(e)
                tt.add_task(Aio_Req(self.url,self.callback,meta=self.meta))
                log.log(self.url + "   " + str(e),"error")
class Sin_Req(object):
    """
    :param url:带抓取链接
    :param callback: 回调函数
    :param meta: 需要函数间传递的参数
    """
    def __init__(self,url,callback,meta = {}):
        self.url = url
        self.callback = callback
        self.meta = meta
        self.headers = {"User-Agent": random.choice(agents)}
    def get(self):
        try:
            r = requests.get(url=self.url,headers = self.headers,proxies = PROXIES)
            log.log(str(r.status_code)+"   "+self.url,"info")
            self.meta["response"] = r.text
            self.callback(self.meta)
            # tt.old_task(self.url)
        except Exception as e:
            tt.add_task(Sin_Req(self.url, self.callback,meta=self.meta))
            log.log(self.url+"  "+str(e),"error")
if __name__ == '__main__':
    pass



