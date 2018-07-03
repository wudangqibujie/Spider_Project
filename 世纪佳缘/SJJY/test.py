# from m_queue import TaskQueue
# from lxml import etree
#
# tt = TaskQueue()
# from req import Sin_Req
# url = "https://sz.lianjia.com/ershoufang/pg2/"
# def A(response):
#     html = etree.HTML(response["response"])
#     title = html.xpath('//title/text()')
#     print(title)
# rr = Sin_Req(url=url,callback=A)
# import pickle
# tt.add_task(rr)
# a = tt.pop_task()
# a.get()
import pymongo
cl = pymongo.MongoClient()
db = cl["SJJY"]
coll = db["data"]
ls= set()
for i in coll.find():
    ls.add(i["uid"])
print(len(ls))
