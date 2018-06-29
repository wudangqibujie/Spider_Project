import pymongo
client = pymongo.MongoClient()
db = client["AJK_price_trend"]
coll_1 = db["coordin_buchong"]
coll_2 = db["coordin"]
f = open("coo.txt","w")
def create_json(start,stop):
    """
    格式化成百度地图的接入数据标准
    :param start: 开始年份的均价
    :param stop: 结束年份的均价
    :return:
    """
    for i in coll_1.find():
        try:
            data = i["coordin"]
            name = list(i["data"].keys())[0]
            print(i["data"][name])
            data["count"] = (i["data"][name][stop]-i["data"][name][start])*1000
            print(data)
            f.write(str(data)+","+"\n")
        except:
            pass
if __name__ == '__main__':
    create_json("201704","201804")


