from redis  import StrictRedis
# from req import *
import pickle
from settings import *
class TaskQueue(object):
    def __init__(self):
        self.r = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    def add_task(self,req):
        if not self.r.sismember(SPIDER_NAME+"_taskover",req.url):
            self.r.sadd(SPIDER_NAME+"_task",pickle.dumps(req))
    def pop_task(self):
        if self.r.scard(SPIDER_NAME+"_task"):
            a = self.r.spop(SPIDER_NAME+"_task")
            return pickle.loads(a)
    def old_task(self,url):
        self.r.sadd(SPIDER_NAME+"_taskover",url)
    def reload(self):
        self.r.delete(SPIDER_NAME+"_taskover")
        self.r.delete(SPIDER_NAME+"_items")
        self.r.delete(SPIDER_NAME+"_task")
class Item_Queue(object):
    def __init__(self):
        self.r = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    def add_item(self,item):
        self.r.sadd(SPIDER_NAME+"_items",pickle.dumps(item))
    def pop_item(self):
        if self.r.scard(SPIDER_NAME+"_items"):
            self.r.spop(SPIDER_NAME+"_items")
    def error_item(self,item):
        self.r.sadd(SPIDER_NAME + "_error", pickle.dumps(item))
if __name__ == '__main__':
    t = TaskQueue()
    t.reload()





