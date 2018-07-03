import pymongo
import time
import random
import matplotlib.pyplot as plt
client = pymongo.MongoClient()
db = client["YX_F"]
coll = db["cleaned_report"]

CAR= ['宝马',
      '丰田',
      '大众',
      'Jeep',
      '本田',
      '雷克萨斯',
      '别克',
      '众泰',
      '奥迪',
      'MINI',
      '日产',
      '路虎',
      '雪佛兰',
      '保时捷',
      '凯迪拉克',
      '哈弗',
      '奔驰',
      '玛莎拉蒂',
      '福特',
      'DS',
      '纳智捷',
      '英菲尼迪',
      '比亚迪',
      '斯巴鲁']
COLORS = ["dimgray",
          "orange",
          "lightgreen",
          "cornflowerblue",
          "sandybrown",
          "cadetblue",
          "darkkhaki",
          "coral",
          "burlywood",
          "wheat",
          "lightsteelblue",
          "mediumaquamarine",
          "plum",
          "tomato",
          "skyblue",
          "gold",
          "c",
          "powderblue",
          "darksalmon"]

def get_data(brand):
    data = {"事故排查检测":0,"轻微碰撞检测":0,"启动检测":0,"易损耗部件检测":0,"常用功能检测":0,"外观内饰检测":0,"漆面检测":0}
    sum_ = coll.count({"brand_name":brand})
    for i in coll.find({"brand_name":brand}):
        data["事故排查检测"] += i["about_pro"]["事故排查检测"][1]
        data["轻微碰撞检测"] += i["about_pro"]["轻微碰撞检测"][1]
        data["启动检测"] += i["about_pro"]["启动检测"][1]
        data["易损耗部件检测"] += i["about_pro"]["易损耗部件检测"][1]
        data["常用功能检测"] += i["about_pro"]["常用功能检测"][1]
        data["外观内饰检测"] += i["about_pro"]["外观内饰检测"][1]
        data["漆面检测"] += i["about_pro"]["漆面检测"][1]
    for k in data.keys():
        data[k] = data[k]/sum_
    return data

def bar_graph(x_data,y_data,title_name,file_name,color,x_label,y_label,x_l_lim = None,x_h_lim=None,y_l_lim = None,y_h_lim = None):
    plt.figure(figsize=(15, 6), dpi=200, frameon=False)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    x_ = range(len(y_data))
    rec_gr = plt.bar(x=x_data,height = y_data,width = 0.2,color = color,label = "A")
    plt.ylim(y_l_lim,y_h_lim)
    plt.xlim(x_l_lim,x_h_lim)
    plt.xlabel(x_label,size = 18,)
    plt.ylabel(y_label,size = 18)
    plt.xticks(rotation=28)
    plt.title(title_name,loc = "right",fontsize = 17,fontweight = "medium")
    plt.savefig("{}.jpg".format(file_name))
    plt.close()

def about_pro_graph(item):
    data={}
    for i in CAR:
        d = get_data(i)
        data[i] = d[item]
    print(data)
    c = random.choice(COLORS)
    data = sorted(data.items(), key=lambda d: d[1], reverse=True)
    x_data, y_data = [i[0] for i in data], [i[1] for i in data]
    bar_graph(x_data,y_data,item,item,c,"brand","error counts per car")

def error_grapth():
    items = ["事故排查检测", "轻微碰撞检测", "启动检测", "易损耗部件检测", "常用功能检测", "外观内饰检测", "漆面检测"]
    for i in items:
        about_pro_graph(i)

def brand_about_error(brand):
    data = get_data(brand)
    data = sorted(data.items(), key=lambda d: d[1], reverse=True)
    x_data, y_data = [i[0] for i in data], [i[1] for i in data]
    c = random.choice(COLORS)
    bar_graph(x_data, y_data, brand+" flaw situration", brand+"_error rank", c, "flaw item", "error counts per car")

def bran_2_error_graph():
    for i in CAR:
        brand_about_error(i)

def detail_flaw(brand):
    a = coll.find_one({"brand_name":brand})
    print(a["item_lst"])
    items_lst = []
    for i in a["item_lst"]:
        items_lst.append(i["name"])
    print(items_lst)
    data = dict.fromkeys(items_lst,0)
    print(data)
    sum_ = coll.count({"brand_name":brand})
    for j in coll.find({"brand_name":brand}):
        a = j["item_lst"]
        for k in a :
            data[k["name"]]+= k["num"]
    print(data)
    for y in data.keys():
        data[y] = data[y]/sum_
    print(data)
    data = sorted(data.items(), key=lambda d: d[1], reverse=True)
    x_data, y_data = [i[0] for i in data], [i[1] for i in data]
    return x_data,y_data

def detail_graph():
    for i in CAR:
        x,y = detail_flaw(i)
        c=random.choice(COLORS)
        bar_graph(x[:21],y[:21],i+" detail error",i+" detail error",c,"flaw item","flaw nums per car")

if __name__ == '__main__':
    get_data("宝马")
    get_data("奔驰")
    error_grapth()
    bran_2_error_graph()
    detail_flaw("宝马")
    detail_graph()

