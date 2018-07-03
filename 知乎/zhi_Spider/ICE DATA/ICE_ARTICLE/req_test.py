import requests
from lxml import etree
import time
import random
import json
from selenium import webdriver
import pymongo
client = pymongo.MongoClient()
db = client["ICE_DATA"]
coll = db["data"]
coll_comment = db["comment"]
BASE_URL = "https://www.zhihu.com/api/v4/members/shu-ju-bing-shan/activities?limit=7&after_id=1522120267&desktop=True"
HEADERS = {
'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
# 'cookie': '_zap=390b8054-1be5-43c6-a035-491476a201e2; __DAYU_PP=EFuYavQjbVnqFjjRr6jf211d2268c6e9; __utma=51854390.378497535.1524235715.1524235715.1524235715.1; __utmz=51854390.1524235715.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/chen-da-87-94/collections; __utmv=51854390.100-1|2=registration_date=20130630=1^3=entry_date=20130630=1; d_c0="AKBvT1_UiA2PToEY-9eGe7rjWZfXzjJenm8=|1525300777"; q_c1=35cbf7017dd143cf88c77ba79d77c482|1525840291000|1520341732000; _xsrf=f48b6cc2-1553-4ee1-9c1b-176b6afcbd19; capsion_ticket="2|1:0|10:1527905442|14:capsion_ticket|44:NjkxZGRhNzE0OTA1NDg2Njk4YWExMDdkODE3ZWU3ODQ=|d8df3d9de35a5b9b004b7bf6d455d228ec346cb2c79fdf6b29b8e092a8f9888c"; l_n_c=1; n_c=1; l_cap_id="NmQ0MzMzYTRjYWM3NDM5ODgxODM1ODNkMzAyYTY5MDk=|1527910756|d4198447f9cf44a4c35bac92bf825d6e851e51af"; r_cap_id="OGY2MDZmODJkYTNjNDNjMDlkOGFlMDY1ZGVkN2MyNGY=|1527910756|82d623d6cb29214aadf494a82006fa3247254e75"; cap_id="MDI0MDUzODliZGZjNGY5OWE4NTQ2OWU2YjA2Njc4YjY=|1527910756|80daeb89ab1d92e2a8033596c7fe15f39f3a611f"; tgw_l7_route=b3dca7eade474617fe4df56e6c4934a3',
'referer': 'https://www.zhihu.com/org/shu-ju-bing-shan/activities',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
}
# START_ID = 1522120267
def start_get():
    url = "https://www.zhihu.com/org/shu-ju-bing-shan/activities"
    browser = webdriver.Chrome()
    browser.get(url)
    html = etree.HTML(browser.page_source)
    get_start_data(html)
def get_start_data(html):
    items = html.xpath('//div[@class="List-item"]')
    for i in items:
        data = dict()
        action = i.xpath('div[@class="List-itemMeta"]/div[@class="ActivityItem-meta"]/span[1]/text()')[0]
        title = i.xpath('div[@class="ContentItem ArticleItem"]/h2[1]/a/text()')[0]
        link = i.xpath('div[@class="ContentItem ArticleItem"]/@data-zop')[0]
        like_count = i.xpath('div[@class="ContentItem ArticleItem"]/div[@class="ContentItem-meta"]/div[@class="ArticleItem-extraInfo"]/span/button/text()')[0]
        comment_count = i.xpath('div[@class="ContentItem ArticleItem"]/div[@class="RichContent is-collapsed"]/div[@class="ContentItem-actions"]/button[2]/text()')[0]
        abstract = i.xpath('div[@class="ContentItem ArticleItem"]/div[@class="RichContent is-collapsed"]/div[2]/span/text()')
        data["title"] = title
        data["action"] = action
        data["link"] = link
        data["like_count"] = like_count
        data["comment_count"] = comment_count
        data["abstract"] = abstract
        yield data
def next_req(url):
    r = requests.get(url,headers = HEADERS)
    data = json.loads(r.text)
    time.sleep(random.randint(4,9))
    if not data["paging"]["is_end"]:
        for i in data["data"]:
            print(i)
            coll.insert(i)
        next_link = data["paging"]["next"]
        next_req(next_link)
    else:
        for i in data["data"]:
            print(i)
            coll.insert(i)
def get_article_id():
    id_lst = []
    for i in coll.find():
        id_lst.append(i["target"]["id"])
    return id_lst
def get_comment_data(arti_id,offset):
    url = "https://www.zhihu.com/api/v4/articles/{id}/comments?includ\
    e=data%5B*%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting\
    %2Cvote_count%2Cis_parent_author%2Cis_author&order=normal&limit=20&offset={page}&status=open"
    try:
        r = requests.get(url.format(id=arti_id,page=offset*20), headers=HEADERS)
        r.encoding = "utf-8"
        data = json.loads(r.text)
        time.sleep(random.randint(4, 9))
        if not data["paging"]["is_end"]:
            # coll_comment.insert(data)
            print(data)
            data["arti_id"] = arti_id
            # coll_comment.insert(data)
            get_comment_data(arti_id,offset+1)
        else:
            # coll_comment.insert(data)
            print(data)
    except Exception as e:
        print("出错了",arti_id,offset)
def run_comment():
    id_lst = get_article_id()
    for i in id_lst:
        get_comment_data(i,0)
if __name__ == '__main__':
    # next_req(BASE_URL)
    run_comment()

