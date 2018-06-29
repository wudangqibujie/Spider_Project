import pymongo
import matplotlib.pyplot as plt
import datetime
import random
client = pymongo.MongoClient()
db = client["AJK_price_trend"]
coll_1 = db["price_trend"]
colors = ["dimgray",
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

def get_city():
    """
    :return:得到每个城市的均价变化数据
    """
    city = set()
    for i in coll_1.find():
        aa = i["data"].keys()
        data = {}
        try:
            if len(list(aa)[1]) != 5:
                data[list(aa)[1]] = i["data"][list(aa)[1]]
                city.add(str(data))
        except Exception as e:
            print("出错",e)
    aa = list(city)
    return aa

def bar_graph(x_data,y_data,title_name,file_name,color,x_label,y_label,x_l_lim = None,x_h_lim=None,y_l_lim = None,y_h_lim = None):
    plt.figure(figsize=(15, 6), dpi=200, frameon=False)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    rec_gr = plt.bar(x=x_data,height = y_data,width = 3,color = color)
    plt.ylim(y_l_lim,y_h_lim)
    plt.xlim(x_l_lim,x_h_lim)
    plt.plot(x_data,y_data,linestyle='--')
    plt.xlabel(x_label,size = 18)
    plt.ylabel(y_label,size = 18)
    plt.xticks(rotation=20)
    plt.title(title_name,loc = "right",fontsize = 17,fontweight = "medium")
    plt.savefig("{}.jpg".format(file_name))
    plt.close()

def city_graph(obj):
    """
    每座城市的均价变化曲线图
    :param obj:每个城市的历史均价基础数据
    :return:单个城市的均价变化趋势图
    """
    obj = eval(obj)
    title = list(obj.keys())[0][:-5]
    time_ = obj[list(obj.keys())[0]].keys()
    price = list(obj[list(obj.keys())[0]].values())
    time_1 = [i[:4] + " "+ i[-2:] for i in time_]
    time_2 = [datetime.datetime.strptime(i,'%Y %m') for i in time_1]
    print(price)
    for i in range(len(price)):
        if price[i] == None:
            price[i] = 0
    print(title)
    print(time_2)
    print(price)
    bar_graph(time_2,price,title,title,random.choice(colors),"Year","Price")

def city_compare():
    """
    四座一线城市历史均价变化对比
    :return:
    """
    plt.figure(figsize=(15, 6), dpi=200, frameon=False)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    aa = []
    bb = []
    for i in get_city():
        if "深圳" in i or "上海" in i or "北京" in i or "广州" in i:
            aa.append(eval(i))
    for k in aa:
        if '上海市-0001' in k:
            if k['上海市-0001']["201806"]>5.03:
                bb.append(k)
        if "深圳-0400" in k:
            if k['深圳-0400']['201806'] > 4.9:
                bb.append(k)
        if "广州-0200" in k:
            if k['广州-0200']['201806'] > 2.9:
                bb.append(k)
        if '北京-0600' in k:
            bb.append(k)
    for ci in bb:
        title = list(ci.keys())[0][:-5]
        time_ = ci[list(ci.keys())[0]].keys()
        price = list(ci[list(ci.keys())[0]].values())
        time_1 = [i[:4] + " " + i[-2:] for i in time_]
        time_2 = [datetime.datetime.strptime(i, '%Y %m') for i in time_1]
        plt.plot(time_2, price, linestyle='--',label = title)
    plt.legend()
    plt.xlabel("Year", size=18)
    plt.ylabel("Price", size=18)
    plt.xticks(rotation=0)
    plt.title("City Compare", loc="right", fontsize=17, fontweight="medium")
    plt.savefig("{}.jpg".format("City Compare"))
    plt.close()

def zone_compare():
    """
    四个一线城市，各自每个区属的均价历史数据对比
    :return:
    """
    city_lst = ["北京-0600","上海市-0001","深圳-0400","广州-0200"]
    for city in city_lst:
        plt.figure(figsize=(15, 6), dpi=200, frameon=False)
        plt.rcParams['font.sans-serif'] = ['SimHei']
        zone = set()
        data = set()
        for j in db["price_trend_buchong"].find():
            if city in j["data"].keys():
                zone.add(list(j["data"].keys())[2])
        for i in db["price_trend_buchong"].find():
            for z in list(zone):
                if z in i["data"].keys():
                    aa = dict()
                    aa[z] = i["data"][z]
                    data.add(str(aa))
        for ci in list(data):
            ci = eval(ci)
            title = list(ci.keys())[0][:-9]
            time_ = ci[list(ci.keys())[0]].keys()
            price = list(ci[list(ci.keys())[0]].values())
            time_1 = [i[:4] + " " + i[-2:] for i in time_]
            time_2 = [datetime.datetime.strptime(i, '%Y %m') for i in time_1]
            plt.plot(time_2, price, linestyle='--', label=title)
        plt.legend()
        plt.xlabel("Year", size=18)
        plt.ylabel("Price", size=18)
        plt.xticks(rotation=0)
        plt.title(city[:-5], loc="right", fontsize=17, fontweight="medium")
        plt.savefig("{}.jpg".format(city))
        plt.close()

if __name__ == '__main__':
    # for i in get_city():
    #     city_graph(i)
    # city_compare()
    # zone_compare()
    for i in get_city():
        print(i)