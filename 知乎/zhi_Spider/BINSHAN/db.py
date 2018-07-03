from settings import *
import pymongo

class Mon(object):
    def __init__(self):
        self.client = pymongo.MongoClient(MONGO_HOST,MONGO_PORT)
        self.db = self.client[MONGO_DB_NAME]
    def insert(self,coll_name,data):
        self.db[coll_name].insert(data)
    def data_find(self,coll_name):
        for i in self.db[coll_name].find():
            yield i
    def close(self):
        self.client.close()
