import json
from urllib.request import urlopen, quote
import requests,csv
import re
import pymongo
import pandas as pd

client = pymongo.MongoClient()
db = client["LJ_Spider"]
coll_co_shanghai = db["shanghai_cood"]
city_lst =[ 'guangzhou', 'zhongshan', 'beijing', 'dongguan', 'foshan', 'shanghai', 'zhuhai', 'shenzhen', 'huizhou']
coll = db["shanghai"]
def getlnglat(address):
    url = 'http://api.map.baidu.com/geocoder/v2/'
    output = 'json'
    ak = 'ESP9WBipoQkGmhR1RP5878A7sk71zX4M'
    add = quote(address) #由于本文城市变量为中文，为防止乱码，先用quote进行编码
    # print(add)
    uri = url + '?' + 'address=' + add  + '&output=' + output + '&ak=' + ak
    req = urlopen(uri)
    res = req.read().decode() #将其他编码的字符串解码成unicode
    # print(res)
    return eval(res)["result"]["location"]
f = open("shanghai.txt","w")
e = open("shanghai_error","w",encoding="utf-8")
for i in coll.find():
    try:
        # print(i["address"])
        addr = "上海 "+i["address"]
        data = getlnglat(addr)
        data["count"] = i["uni_price"]
        print(data)
        coll_co_shanghai.insert(data)
        # f.write(str(data)+"\n")
        # f.flush()
        print("OK")
    except:
        e.write(str(i)+"\n")
        e.flush()

