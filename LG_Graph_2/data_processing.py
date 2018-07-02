import pymongo
import re
client = pymongo.MongoClient()
db = client["LG"]
coll = db["raw_data"]
coll1= db["cleaned_data"]

work_year_label = {"1-3年":(1,3),"3-5年":(3,5),"5-10年":(5,10),"应届毕业生":"","不限":None,"1年以下":(None,1),"10年以上":(10,None)}

def get_data():
    for i in coll.find():
        data = dict()
        data["pose_id"] = i["positionId"]
        data["com_id"] = i["companyId"]
        data["work_year"] = work_year_label[i["workYear"]]
        data["com_name"] = i["companyShortName"]
        data["advan"] = i["positionAdvantage"]
        a = re.findall(r'(\d+).*?k-(\d+).*?k$', i["salary"], re.I)
        raw_salary = a if a else re.findall(r'(.*?)k以上$',i["salary"])
        salary = (int(raw_salary[0][0]),int(raw_salary[0][1])) if isinstance(raw_salary[0],tuple) else (int(raw_salary[0]),None)
        data["salary"] = salary
        data["edu"] = i["education"]
        data["city"] = i["city"]
        data["longitude"] = i["longitude"]
        data["latitude"] = i["latitude"]
        data["financeStage"] = i["financeStage"]
        data["com_label"] = i["companyLabelList"]
        data["district"] = i["district"]
        data["com_size"] = i["companySize"]
        data["pose_label"] = i["positionLables"]
        data["resume_rate"] = i["resumeProcessRate"]
        data["com_full_name"] = i["companyFullName"]
        data["pose_type"] = i["pose_type"]
        yield data

for i in get_data():
    coll1.insert(i)

if __name__ == '__main__':
    get_data()







# for i in coll.find({},{"salary":1}):
#     a = re.findall(r'(\d+).*?k-(\d+).*?k$',i["salary"],re.I)
#
#     if not a:
#         b = re.findall(r'(.*?)k以上$',i["salary"])
#         if not b:
#             print(b)
#     else:
#         pass
