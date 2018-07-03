import pymongo
import time
client = pymongo.MongoClient()
db = client["YX_F"]
coll_data = db["cleaned_data"]
coll_report = db["report"]
coll_cleaned_report = db["cleaned_report"]
def get_pro_lst(data):
    b = data["report"]["data"]["report_category"]
    data_1 = {}
    item_lst = []
    problem_lst = []
    for i in b:
        c = i["child"]
        data_1[i["cat_name"]] = [i["all_num"],i["flaw_all_num"],i["flaw_all_num"]/i["all_num"]]
        for j in c:
            for h in j["child"]:
                data_item = {}
                if "flaw_num" in h.keys():
                    data_pro = dict()
                    data_pro["cat_name"] = h["cat_name"]
                    data_pro["nums"] = h["flaw_num"]
                    data_pro["flaw_name"] = h["flaw_code_describe"]
                    problem_lst.append(data_pro)
                if "flaw_num" in h.keys():
                    data_item["name"] = h["cat_name"]
                    data_item["num"] = h["flaw_num"]
                    data_item["flaw_name"] = h["flaw_code_describe"]
                else:
                    data_item["name"] = h["cat_name"]
                    data_item["num"] = 0
                item_lst.append(data_item)
    return data_1,problem_lst,item_lst
def proess():
    for i in coll_report.find():
        data = {}
        if i["report"]["data"]:
            id = i["car_id"]
            data["id"] = id
            d = coll_data.find({"car_id":id}).next()
            data["brand"] = d["brand_id"]
            data["series"] = d["series_id"]
            data["brand_name"] = d["title"].split()[0]
            data["series_name"] = d["title"].split()[1]
            data["name"] = d["title"]
            a,b,c = get_pro_lst(i)
            data["about_pro"] = a
            data["pro_lst"] = b
            data["item_lst"] = c
            coll_cleaned_report.insert(data)
if __name__ == '__main__':
    proess()
