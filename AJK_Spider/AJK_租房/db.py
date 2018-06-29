from settings import *
import pymongo

class Mon(object):
    def __init__(self):
        self.client = pymongo.MongoClient(MONGO_HOST,MONGO_PORT)
        self.db = self.client[MONGO_DB_NAME]
    def insert(self,coll_name,data):
        """
        数据的插入
        :param coll_name:插入MongoDB内的集合名字
        :param data: 需要持久化的字典结构数据
        :return:
        """
        self.db[coll_name].insert(data)
    def close(self):
        self.client.close()