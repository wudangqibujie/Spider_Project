import aiohttp
import requests
import redis
import asyncio
from settings import *
import time
from requests import Request
from lxml import etree
import pickle
from m_queue import TaskQueue
import random
from log import log
tt = TaskQueue()
class Aio_Req(object):
    def __init__(self,url,callback,meta = {}):
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
class Post_Req(object):
    def __init__(self,url,post_data,params_data,callback,meta = {}):
        self.url = url
        self.callback = callback
        self.meta = meta
        self.param = params_data
        self.headers = {"User-Agent": random.choice(agents)}
        self.post_data = post_data
    def get(self):
        try:
            r = requests.post(url=self.url,data = self.post_data,params = self.param,headers = self.headers,proxies = PROXIES)
            log.log(str(r.status_code)+"   "+self.url,"info")
            self.meta["response"] = r.text
            time.sleep(3)
            self.callback(self.meta)
        except Exception as e:
            tt.add_task(Post_Req(self.url,self.post_data,self.param,self.callback,meta=self.meta))
            log.log(self.url+"  "+str(e),"error")
if __name__ == '__main__':
    pass



