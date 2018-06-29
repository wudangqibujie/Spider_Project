import pymongo
import numpy as np
import random
import pandas as pd
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import datetime as dt
from datetime import datetime

client = pymongo.MongoClient()
db = client["AKQC"]
coll = db["cleaned_data"]
car = ["Audi A4L",
       "Audi A6L",
       "Audi A8L",
       "BMW 3 Series",
       "BMW 5 Series",
       "BMW 7 Series",
       "Benz C class",
       "Benz E class",
       "Benz S class",
       "Audi Q5",
       "Benz GLC",
       "Benz GLK",
       "BMW X3"]
Color = ['lightgreen',
         'gold',
         'lightskyblue',
         'lightcoral',
         'lightgray',
         'lightyellow',
         'lightpink',
         'lightslategray',
          'lemonchiffon',
         'lawngreen',
         'linen',
         'lightseagreen',
         'lavenderblush']

def get_data():
    for i in coll.find():
        yield i

def share():
    """
    BBA各个系的关注比例
    :return:
    """
    counts = {k:coll.count({"car":k}) for k in car}
    audi_counts = {k:counts[k] for k in car if "Audi" in k}
    bmw_counts = {k:counts[k] for k in car if "BMW" in k}
    benz_counts = {k:counts[k] for k in car if "Benz" in k}
    brand_counts = {"Benz":sum(benz_counts.values()),"BMW":sum(bmw_counts.values()),"Audi":sum(audi_counts.values())}
    colors = ['lightgreen', 'gold', 'lightskyblue', 'lightcoral','lightgray','lightyellow','lightpink','lightslategray','lemonchiffon','lawngreen','linen','lightseagreen','lavenderblush']
    pie_graph(audi_counts,colors,"BBS Share of AUDI","BBS of Audi Share")
    pie_graph(bmw_counts,colors,"BBS Share of BMW","BBS of BMW Share")
    pie_graph(brand_counts,colors,"BBS Share of Brand","BBS of Brand Share")
    pie_graph(benz_counts,colors,"BBS Share of BENZ","BBS of Benz Share")

def pie_graph(obj,colors,filename,title):
    """
    饼图
    :param obj:
    :param colors:
    :param filename:
    :param title:
    :return:
    """
    labels = list(obj.keys())
    values = list(obj.values())
    plt.title(title,loc = "left",fontsize=17,fontweight="medium")
    plt.rcParams['font.sans-serif'] = ['SimHei']
    explode = [0.05 for _ in range(len(obj))]
    plt.pie(values, explode=explode, labels=labels, colors=colors,autopct='%1.1f%%', shadow=True, startangle=50)
    plt.axis('equal')
    plt.savefig("{}.jpg".format(filename))
    plt.close()

def scatter_graph(x_data,y_data,title,item):
    """
    散点图
    :param x_data:
    :param y_data:
    :param title:
    :param item:
    :return:
    """
    fig = plt.figure(figsize = (9.5,7.5),dpi=200,frameon=False)
    ax1 = fig.add_subplot(111)
    ax1.set_title(title,loc="right", fontsize=13, fontweight="medium")
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.xlim(datetime(2005, 1, 1, 0, 0), datetime(2018, 3, 1, 0, 0))
    y_lim = 100000 if item == " views" else 500
    plt.ylim(0, y_lim)
    plt.xlabel("Time")
    plt.ylabel(item+"_nums")
    ax1.scatter(x_data,y_data,c='lightgreen', marker='o', s=0.5)
    plt.savefig("{}.jpg".format(title+" "+item))
    plt.close()

def time_squence_graph(data,brand,series,item):
    """
    :param data: 从数据库导入进来的数据
    :param brand: 汽车品牌
    :param series: 品牌系列
    :param item: 评论数/点击数
    :return: 返回对应的时间序列和评论数序列/点击数序列
    """
    x_data = []
    y_data = []
    for i in data:
        if brand in i["car"] and series in i["car"]:
            x_data.append(i["post_time"])
            y_data.append(i[item])
    return x_data,y_data

def uni_comm_view():
    """
    生成每个车系列的评论数/点击数在时间序列上的变化散点图
    :return:
    """
    car_series = {"Benz": ["C class", "E class", "S class", "GLC"], "BMW": ["3 Series", "5 Series", "7 Series", "X3"],
                  "Audi": ["A4L", "A6L", "A8L", "Q5"]}
    items = ["comment", "views"]
    for k, v in car_series.items():
        for i in v:
            for j in items:
                x, y = time_squence_graph(get_data(), k, i, j)
                scatter_graph(x, y, k + " of " + i, " " + j)

def brand_compare(brands,item,color,filename,y_lim):
    """
    不同品牌的每个车系的评论数/点击数在时间序列上的对比，散点图
    :param brands: 品牌车系
    :param item: 评论/点击
    :param color: 绘图的颜色
    :param filename: 保存成的文件名字
    :param y_lim: Y轴数据的上限控制
    :return:
    """
    fig = plt.figure(figsize = (18,12),dpi=100,frameon=False)
    nums = str(len(brands))+"1"
    start = 0
    for i in brands:
        x_data,y_data = [],[]
        p = fig.add_subplot(eval(nums+str(start+1)))
        for j in get_data():
            if i in j["car"]:
                x_data.append(j["post_time"])
                y_data.append(j[item])
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.title("Distribution of "+i, loc="right", fontsize=15, fontweight="medium")
        plt.xlim(datetime(2005,1,1,0,0), datetime(2018,3,1,0,0))
        plt.ylim(0, y_lim)
        plt.xlabel('Time',size=15)
        plt.ylabel(item,size=15)
        p.scatter(x_data,y_data,c=color, marker='o', s=1)
        start += 1
    plt.savefig("Distribution of {}.jpg".format(filename))

def get_distri():
    """
    生成每个品牌的各系列的评论数和点击数的散点图对比
    :return:
    """
    items = ["comment","views"]
    coment_y_lim = 500
    view_y_lim = 1000000
    for i in items:
        brand_compare(["BMW 3 Series", 'BMW 5 Series', 'BMW 7 Series'], i,Color[2],"BMW_"+i+"_distri.jpg",coment_y_lim if i=="comment" else view_y_lim)
        brand_compare(["Benz C class", "Benz E class", "Benz S class"], i, Color[3], "Benz_" + i + "_distri.jpg",coment_y_lim if i=="comment" else view_y_lim)
        brand_compare(["Audi A4L", "Audi A6L", "Audi A8L"], i, Color[0], "Audi_" + i + "_distri.jpg",coment_y_lim if i=="comment" else view_y_lim)
        brand_compare(["Audi Q5", "BMW X3", "Benz GLC"], i, Color[1], "Medium SUV_" + i + "_distri.jpg",coment_y_lim if i=="comment" else view_y_lim)
        brand_compare(["Audi", "BMW", "Benz"], i, Color[1], "Brand_" + i + "_distri.jpg",coment_y_lim if i=="comment" else view_y_lim)
        brand_compare(["Audi A4L", "BMW 3 Series", "Benz C class"], i, "lightblue", "A car_" + i + "_distri.jpg",coment_y_lim if i=="comment" else view_y_lim)
        brand_compare(["Audi A6L", "BMW 5 Series", "Benz E class"], i, Color[-4], "B car_" + i + "_distri.jpg",coment_y_lim if i=="comment" else view_y_lim)
        brand_compare(["Audi A8L", "BMW 7 Series", "Benz S class"], i,"lime", "C car_" + i + "_distri.jpg",coment_y_lim if i=="comment" else 400000)

def together_compare(brands,item,filename,y_lim,start_time=datetime(2005, 1, 1, 0, 0),end_time = datetime(2018, 3, 1, 0, 0)):
    """
    不同车系的评论数点击数，放到同一个散点图中进行对比
    :param brands: 汽车品牌
    :param item: 评论数/点击数
    :param filename: 文件名
    :param y_lim: 上限控制
    :param start_time: 开始时间
    :param end_time: 结束时间
    :return:
    """
    colors = [Color[1],Color[2],Color[3]]
    plt.figure(figsize = (9.5,7.5),dpi=200,frameon=False)
    nums = 0
    plt.subplot(111)
    for i in brands:
        x_data,y_data = [],[]
        for j in get_data():
            if i in j["car"]:
                x_data.append(j["post_time"])
                y_data.append(j[item])
        plt.xlim(start_time,end_time)
        plt.title("Distribution Comparison of "+" ".join(brands), loc="right", fontsize=11, fontweight="medium")
        plt.xlabel('Time', size=11)
        plt.ylabel(item, size=11)
        plt.ylim(0, y_lim)
        plt.scatter(x_data,y_data, c=colors[nums], label=i, marker='o', s=0.1)
        nums += 1
        plt.legend()
    plt.savefig("Together Distribution of {item} of {name}.jpg".format(item=item,name=filename))
    plt.close()

def together_distri():
    """
    生成散点对比图
    :return:
    """
    items = ["comment", "views"]
    for i in items:
        together_compare(["Audi A8L", "BMW 7 Series", "Benz S class"],i,"C car",100000 if i =="views" else 500)
        together_compare(["Audi A6L", "BMW 5 Series", "Benz E class"],i,"B car",100000 if i =="views" else 500)
        together_compare(["Audi A4L", "BMW 3 Series", "Benz C class"],i,"A car",100000 if i =="views" else 500)
        together_compare(["Audi", "BMW", "Benz"],i,"Brand car",100000 if i =="views" else 500)
        together_compare(["Audi Q5", "BMW X3", "Benz GLC"],i,"SUV",100000 if i =="views" else 500)
        together_compare(["Audi A4L", "Audi A6L", "Audi A8L"],i,"Audi",100000 if i =="views" else 500)
        together_compare(["Benz C class", "Benz E class", "Benz S class"],i,"Benz",100000 if i =="views" else 500)
        together_compare(["BMW 3 Series", 'BMW 5 Series', 'BMW 7 Series'],i,"BMW",100000 if i =="views" else 500)

if __name__ == '__main__':
    share()
    get_distri()
    uni_comm_view()
    together_distri()




