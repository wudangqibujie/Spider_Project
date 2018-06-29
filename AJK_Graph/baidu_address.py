import pymongo
import re
import json
from urllib.request import urlopen, quote
import requests,csv
import pandas as pd
cl = pymongo.MongoClient()
db = cl["AJK_price_trend"]
coll = db["clean"]
E = open("error_address.txt","w",encoding="utf-8")
def getlnglat(address):
    url = 'http://api.map.baidu.com/geocoder/v2/'
    output = 'json'
    ak = 'ESP9WBipoQkGmhR1RP5878A7sk71zX4M'
    add = quote(address) #由于本文城市变量为中文，为防止乱码，先用quote进行编码
    uri = url + '?' + 'address=' + add  + '&output=' + output + '&ak=' + ak
    req = urlopen(uri)
    res = req.read().decode() #将其他编码的字符串解码成unicode
    return eval(res)["result"]["location"]

def get_zuo():
    add_after = []
    for j in db["coordin"].find():
        add_after.append(j["address"])
    for i in coll.find():
        address = i["address"]
        if address not in add_after:
            try:
                coordin = getlnglat(address)
                i["coordin"] = coordin
                print(coordin)
                db["coordin_buchong"].insert(i)
            except Exception as e:
                print(e)
                E.write(address+"\n")
                E.flush()
if __name__ == '__main__':
    get_zuo()



