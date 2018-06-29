import requests
import agent
import time
from lxml import etree
import random
import pymongo
client = pymongo.MongoClient()
db = client["anjuke_F"]
# city_lst = ["佛山","东莞","中山","惠州","北京","哈尔滨","三亚","海口","长沙","武汉","杭州","南京","厦门","合肥","苏州","郑州","大连"]
city_lst = ["成都","天津","长春","鄂尔多斯","福州","贵阳","合肥","吉林","昆明","兰州","陆丰","梅州","南宁","普宁","青岛","泉州","沈阳","顺德","汕尾",
"太原","济南","西安","烟台","珠海"]
coll = db["city"]
base_url = "https://m.anjuke.com/bj/sale/?from=anjuke_home&page={}"
headers = {"User-Agent":random.choice(agent.agents)}
er = open("error.txt","a",encoding="utf-8")
def city(city,url):
    for i in range(1,1001):
        try:
            time.sleep(random.randint(3,7))
            r = requests.get(url.format(i),headers=headers)
            f = open("{city}二手  {page}.html".format(city=city,page=i),"w",encoding="utf-8")
            f.write(r.text)
            f.close()
            print(str(r.status_code)+"  {}  ".format(i)+r.url)
            html = etree.HTML(r.text)
            items = html.xpath('//div[@class="baseinfo"]')
            print(items)
            if not items:
                break
        except Exception as e:
            print(e)
            er.write(city+" "+str(i)+"\n")
            er.flush()
for c in city_lst:
    b_url = coll.find_one({c:{"$regex":".*"}})[c]+"sale/?from=anjuke_home&page={}"
    # print(b_url)
    city(c,b_url)

