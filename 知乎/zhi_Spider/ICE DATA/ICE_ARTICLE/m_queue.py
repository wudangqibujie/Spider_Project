from redis  import StrictRedis
# from req import *
import pickle
from settings import *
class TaskQueue(object):
    def __init__(self):
        self.r = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    def add_task(self, req):
        """
        先判断是否已抓取，然后把新生成的任务加入任务队列
        :param req: Request对象
        :return:
        """
        if not self.r.sismember(SPIDER_NAME + "_taskover", req.url):
            self.r.sadd(SPIDER_NAME + "_task", pickle.dumps(req))
    def pop_task(self):
        """
        从任务队列内取出一个待抓取任务
        :return: 反序列化出一个待运行Request对象
        """
        if self.r.scard(SPIDER_NAME + "_task"):
            a = self.r.spop(SPIDER_NAME + "_task")
            return pickle.loads(a)
    def old_task(self, url):
        """
        把抓取完毕后的链接存入已完成任务队列
        :param url: 已完成链接
        :return:
        """
        self.r.sadd(SPIDER_NAME + "_taskover", url)
    def reload(self):
        """
        调试时所用
        :return:
        """
        self.r.delete(SPIDER_NAME + "_taskover")
        self.r.delete(SPIDER_NAME + "_items")
        self.r.delete(SPIDER_NAME + "_task")
class Item_Queue(object):
    def __init__(self):
        self.r = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    def add_item(self, item):
        self.r.sadd(SPIDER_NAME + "_items", pickle.dumps(item))
    def pop_item(self):
        if self.r.scard(SPIDER_NAME + "_items"):
            self.r.spop(SPIDER_NAME + "_items")
    def error_item(self, item):
        self.r.sadd(SPIDER_NAME + "_error", pickle.dumps(item))


if __name__ == '__main__':
    t = TaskQueue()
    t.reload()



