base_url = "https://api.zhihu.com/people/{u_id}"
import requests
import json
import random
import time
import pymongo
client = pymongo.MongoClient()
db = client["ICE_DATA"]

HEADERS = {
'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
'cookie': '_zap=390b8054-1be5-43c6-a035-491476a201e2; __DAYU_PP=EFuYavQjbVnqFjjRr6jf211d2268c6e9; __utma=51854390.378497535.1524235715.1524235715.1524235715.1; __utmz=51854390.1524235715.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/chen-da-87-94/collections; __utmv=51854390.100-1|2=registration_date=20130630=1^3=entry_date=20130630=1; d_c0="AKBvT1_UiA2PToEY-9eGe7rjWZfXzjJenm8=|1525300777"; q_c1=35cbf7017dd143cf88c77ba79d77c482|1525840291000|1520341732000; _xsrf=f48b6cc2-1553-4ee1-9c1b-176b6afcbd19; capsion_ticket="2|1:0|10:1527905442|14:capsion_ticket|44:NjkxZGRhNzE0OTA1NDg2Njk4YWExMDdkODE3ZWU3ODQ=|d8df3d9de35a5b9b004b7bf6d455d228ec346cb2c79fdf6b29b8e092a8f9888c"; l_n_c=1; n_c=1; l_cap_id="NmQ0MzMzYTRjYWM3NDM5ODgxODM1ODNkMzAyYTY5MDk=|1527910756|d4198447f9cf44a4c35bac92bf825d6e851e51af"; r_cap_id="OGY2MDZmODJkYTNjNDNjMDlkOGFlMDY1ZGVkN2MyNGY=|1527910756|82d623d6cb29214aadf494a82006fa3247254e75"; cap_id="MDI0MDUzODliZGZjNGY5OWE4NTQ2OWU2YjA2Njc4YjY=|1527910756|80daeb89ab1d92e2a8033596c7fe15f39f3a611f"; tgw_l7_route=b3dca7eade474617fe4df56e6c4934a3',
'referer': 'https://www.zhihu.com/org/shu-ju-bing-shan/activities',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
}
user_url = "https://www.zhihu.com/api/v4/columns/hemingke/followers?include=data%5B%2A%5D.follower_count%2Cgender%2Cis_followed%2Cis_following&limit=10&offset={}"

def user_list(offset):
    r = requests.get(user_url.format(offset),headers = HEADERS)
    data = json.loads(r.text)
    return data
def user_item():
    o = 0
    while True:
        # time.sleep(1.2)
        data = user_list(o)
        o += 1
        db["user_lst"].insert(data)
        print(o, "   ", data)
        if data["paging"]["is_end"]:
            break
def user_lst_re_into():
    for i in db["user_lst"].find():
        # print(i["data"])
        for j in i["data"]:
            print(j)
            db["user_base"].insert(j)
def user_detail():
    uu = set()
    for i in db["user_base"].find():
        uu.add(i["id"])
    print(len(uu))
    # for j in uu:
    #     try:
    #         r = requests.get(base_url.format(u_id=j),headers = HEADERS)
    #         data = json.loads(r.text)
    #         print(data)
    #         db["user_info"].insert(data)
    #     except Exception as e:
    #         print(e)
    #         f = open("error.txt","a")
    #         f.write(j+"\n")
    #         f.flush()
if __name__ == '__main__':
    # user_lst_re_into()
    user_detail()
    pass