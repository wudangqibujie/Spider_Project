from settings import *
import pymongo

class Mon(object):
    def __init__(self):
        self.client = pymongo.MongoClient(MONGO_HOST,MONGO_PORT)
        self.db = self.client[MONGO_DB_NAME]
    def insert(self,coll_name,data):
        self.db[coll_name].insert(data)
    def close(self):
        self.client.close()