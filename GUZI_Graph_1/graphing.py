import pymongo
import numpy as np
import random
import pandas as pd
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import datetime as dt
from datetime import datetime
client = pymongo.MongoClient()
car_ = ["Jeep",
        "奥迪",
        "宝马",
        "保时捷",
        "奔驰",
        "比亚迪",
        "别克",
        "大众",
        "法拉利",
        "丰田",
        "福特",
        "捷豹",
        "凯迪拉克",
        "雷克萨斯",
        "路虎",
        "马自达",
        "玛莎拉蒂",
        "日产",
        "斯巴鲁",
        "特斯拉",
        "沃尔沃",
        "五菱",
        "现代",
        "雪佛兰",
        "雪铁龙",
        "英菲尼迪",
        "众泰"]
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

db = client["GUAZI"]
coll = db["cleaned_data"]

def get_data(query=None):
    """
    :param query:MongoDB查询表达式
    :return: 返回查询的数据
    """
    for i in coll.find(query):
        yield i

def get_series_lst(brand):
    """
    :param brand:汽车品牌
    :return:某品牌下的所有车系名称
    """
    data = set()
    for i in get_data({"car":brand}):
        series = i["car_info"][0].replace(brand,"")
        data.add(series)
    return list(data)

def bar_graph(x_data,y_data,title_name,file_name,color,x_label,y_label,x_l_lim = None,x_h_lim=None,y_l_lim = None,y_h_lim = None):
    """条形图"""
    plt.figure(figsize=(15, 6), dpi=200, frameon=False)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    rec_gr = plt.bar(x=x_data,height = y_data,width = 0.2,color = color,label = "A")
    plt.ylim(y_l_lim,y_h_lim)
    plt.xlim(x_l_lim,x_h_lim)
    plt.xlabel(x_label,size = 18)
    plt.ylabel(y_label,size = 18)
    plt.xticks(rotation=20)
    plt.title(title_name,loc = "right",fontsize = 17,fontweight = "medium")
    plt.savefig("{}.jpg".format(file_name))
    plt.close()

def brand_count_rank():
    """
    不同品牌的挂牌数量对比
    :return:
    """
    data = {}
    for c in car_:
        data[c] = coll.count({"car": c})
    data_ = sorted(data.items(), key=lambda d: d[1], reverse=True)
    x_data, y_data = [i[0] for i in data_], [i[1] for i in data_]
    bar_graph(x_data,y_data,"Rank of Brand Counts","Rank of brand",colors[0],"brand","counts")

def test_series(brand):
    """
    :param brand:
    :return:
    """
    data = {}
    series = get_series_lst(brand)
    for i in series:
        data[i] = coll.count({"car":brand,"car_info.0":{"$regex":i}})
    print(data)

def scatter_graph(x_data,y_data,title,filename,x_label,y_label,c):
    """散点图"""
    fig = plt.figure(figsize=(9.5, 7.5), dpi=200, frameon=False)
    ax1 = fig.add_subplot(111)
    ax1.set_title(title, loc="right", fontsize=13, fontweight="medium")
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # plt.ylim(y_l_lim, y_h_lim)
    # plt.xlim(0,1)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    ax1.scatter(x_data, y_data, c=c, marker='o', s=0.5)
    plt.savefig("{}.jpg".format(filename))
    plt.close()
def salvage_graph(brand):
    """
    :param brand:某个品牌
    :return: 生成某个品牌的残值率散点图
    """
    x_data,y_data = [],[]
    for i in coll.find({"car":brand}):
        if (i["ex_price"]) and (i["age"]):
            x_data.append(i["age"])
            y_data.append((i["ex_price"]-i["price"])/i["ex_price"])
    print(x_data)
    print(y_data)
    scatter_graph(x_data,y_data,brand+"salvage with age",brand+" salvage age","age","salvage",random.choice(colors))

def all_salva_grapth():
    """
    :return:生成所有品牌的残值率随里程数的散点图
    """
    for i in car_:
        salvage_graph(i)
def salvage_year(brand):
    """
    :param brand:
    :return:生成残值率随着年份变化的散点图
    """
    x_data, y_data = [], []
    for i in coll.find({"car": brand}):
        if (i["ex_price"]) and (i["year"]):
            x_data.append(i["year"])
            y_data.append((i["ex_price"] - i["price"]) / i["ex_price"])
    print(x_data)
    print(y_data)
    scatter_graph(x_data, y_data, brand + "salvage with year", brand + " salvage year", "year", "salvage",random.choice(colors))

def all_sal_year():
    """
    :return:生成所有品牌的残值率随着年份变化的散点图
    """
    for i in car_:
        salvage_year(i)

def compare_sal_age(brands):
    """
    不同品牌之间的残值率对比
    :param brands: 需要对比的品牌
    :return: 生成散点图
    """
    co = ['peru','lightgreen',"gold","maroon"]
    fig = plt.figure(figsize=(10, 8), dpi=700, frameon=False)
    sum = 0
    plt.rcParams['font.sans-serif'] = ['SimHei']
    for j in brands:
        x_data, y_data = [], []
        for i in coll.find({"car":j}):
            if (i["ex_price"]) and (i["age"]):
                x_data.append(i["age"])
                y_data.append((i["ex_price"] - i["price"]) / i["ex_price"])
        print(x_data)
        print(y_data)
        plt.scatter(x_data, y_data, c=co[sum], label=j, marker='o', s=0.2)
        sum += 1
        plt.xlabel('age', size=13)
        plt.ylabel("salvage", size=13)
        plt.legend()
    title = " ".join(brands)
    plt.title("Salvage Comparison with Age of {}".format(title), loc="right", fontsize=11, fontweight="medium")
    plt.savefig("{} compare age.jpg".format(title))
    plt.close()

def compare_scatter():
    compare_sal_age(["宝马", "奔驰"])
    compare_sal_age(["宝马", "奥迪"])
    compare_sal_age(["奥迪", "奔驰"])
    compare_sal_age(["宝马", "奔驰","奥迪"])
    compare_sal_age(["大众", "丰田"])
    compare_sal_age(["宝马", "雷克萨斯"])
    compare_sal_age(["雷克萨斯", "奔驰"])
    compare_sal_age(["奥迪", "雷克萨斯"])
    compare_sal_age(["路虎", "奔驰"])
    compare_sal_age(["宝马", "路虎"])
    compare_sal_age(["英菲尼迪", "雷克萨斯"])
    for i in car_:
        compare_sal_age(["丰田",i])

def city(brand):
    """
    返回某个品牌在不同地方的挂牌量条形图
    :param brand:
    :return:
    """
    city = set()
    for i in coll.find({"car":brand}):
        city.add(i["city"])
    print(city)
    print(len(city))
    data = dict.fromkeys(list(city))
    for i in list(city):
        data[i] = coll.count({"car":brand,"city":i})
    print(data)
    data_ = sorted(data.items(), key=lambda d: d[1], reverse=True)
    x_data, y_data = [i[0] for i in data_][:21], [i[1] for i in data_][:21]
    color = random.choice(colors)
    print(color,brand+" counts of city")
    bar_graph(x_data,y_data,brand+" counts of city",brand+" counts of city",color,"city","nums")

def city_counts():
    for i in car_:
        city(i)

def SUV_city(brand,query):
    """
    :param brand:品牌名
    :param query: 找到车型的查询条件
    :return: 返回一个车系的城市挂牌量条形图
    """
    data = {}
    city = set()
    for i in coll.find({"car": brand}):
        city.add(i["city"])
    print(city)
    print(len(city))
    data = dict.fromkeys(list(city))
    for i in  list(city):
        data[i] = coll.count({"$or":[{"car":brand,"city":i,"car_info.0":{"$regex":query}},{"car":brand,"city":i,"car_info.1":{"$regex":query}}]})
    data_ = sorted(data.items(), key=lambda d: d[1], reverse=True)
    x_data, y_data = [i[0] for i in data_][:21], [i[1] for i in data_][:21]
    color = random.choice(colors)
    bar_graph(x_data, y_data, query+ " counts of city", brand +query+ " counts of city", color, "city", "nums")

def SUV_graph():
    SUV_city("宝马","X5")
    SUV_city("宝马","X3")
    SUV_city("奔驰","GLE")
    SUV_city("丰田","兰德酷路泽")
    SUV_city("丰田","普拉多")
    SUV_city("斯巴鲁","森林人")
    SUV_city("奥迪","Q7")
    SUV_city("保时捷","卡宴")

if __name__ == '__main__':
    brand_count_rank()
    test_series("奔驰")
    all_salva_grapth()
    all_sal_year()
    compare_scatter()
    city_counts()
    SUV_graph()





