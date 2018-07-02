import pymongo
import numpy as np
import random
import pandas as pd
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import datetime as dt
from datetime import datetime

city = ['北京',
        '上海',
        '深圳',
        '广州',
        '杭州',
        '成都',
        '南京',
        '武汉',
        '西安',
        '厦门',
        '长沙',
        '苏州',
        '天津']
pose = ['oracle',
        '.net',
        '自然语言处理',
        'asp',
        '深度学习',
        '图像处理',
        'ios',
        '语音识别',
        'ruby',
        '自动化测试',
        'sqlserver',
        'go',
        'java',
        '搜索算法',
        'c',
        'c#',
        '机器学习',
        '测试工程师',
        'hive',
        'node.js',
        'web前段',
        '算法工程师',
        'web前端',
        'perl',
        'python',
        'c++',
        '区块链',
        'hadoop',
        'delphi',
        '图像识别',
        'mysql',
        '数据挖掘',
        '机器视觉',
        '运维工程师',
        'php',
        'mongodb',
        'android'
        ]
client = pymongo.MongoClient()
db = client["LG"]
colors = ['lightgreen',
          'gold',
          'lightskyblue',
          'lightcoral',
          'lightgray',
          'lightpink',
          'lightslategray',
           'lawngreen',
          'lightseagreen']
coll = db["cleaned_data"]

def get_data():
    for i in coll.find():
        yield i

def city_big_share():
    """
    :return:生成所抓取的职位数量，不同城市的占比，绘制出饼图
    """
    data = {}
    for i in city:
        data[i] = coll.count({"city":i})
    pie_graph(data,colors,"big share of city","Big Share of City")

def pie_graph(obj,colors,filename,title):
    """饼图"""
    labels = list(obj.keys())
    values = list(obj.values())
    plt.title(title,loc = "left",fontsize=17,fontweight="medium")
    plt.rcParams['font.sans-serif'] = ['SimHei']
    explode = [0.05 for _ in range(len(obj))]
    plt.pie(values, explode=explode, labels=labels, colors=colors,autopct='%1.1f%%', shadow=True, startangle=50)
    plt.axis('equal')
    plt.savefig("{}.jpg".format(filename))
    plt.close()

def pose_city_rec(pose):
    """
    :param pose:职位类型
    :return:返回特定职位在不同城市中的招聘数量，绘制出条形图
    """
    plt.figure(figsize=(12, 6), dpi=200, frameon=False)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    data = {}
    for c in city:
        data[c] = coll.count({"city":c,"pose_type":pose})
    label = list(data.keys())
    value = list(data.values())
    x = range(len(value))
    color = random.choice(colors)
    rec_gr = plt.bar(x = label,height = value,width = 0.4,alpha = 0.8,color = color,label = pose)
    plt.ylim()
    plt.ylabel("pose nums",size = 18)
    plt.xlim()
    plt.xlabel("city",size = 18)
    plt.title(pose+" nums of city ",loc = "right",fontsize=17,fontweight="medium")
    # plt.legend(pose.upper())
    # plt.show()
    plt.savefig("{} nums of city.jpg".format(pose))
    plt.close()

def pose_city_share():
    for i in pose:
        pose_city_rec(i)

def city_pose_rec(city):
    """
    :param city: 城市
    :return: 特定城市下的职位类型招聘数量，生成条形图
    """
    plt.figure(figsize=(15, 6), dpi=200, frameon=False)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    data = {}
    for c in pose:
        data[c] = coll.count({"pose_type":c,"city":city})
    label = list(data.keys())
    value = list(data.values())
    x = range(len(value))
    color = random.choice(colors)
    rec_gr = plt.bar(x = label,height = value,width = 0.1,alpha = 0.8,color = color,label = pose)
    plt.ylim()
    plt.ylabel("city",size = 18)
    plt.xlim()
    plt.xticks(rotation=70)
    plt.xlabel("pose nums",size = 18)
    plt.title(city +" nums of pose ",loc = "right",fontsize=17,fontweight="medium")
    # plt.legend(pose.upper())
    # plt.show()
    plt.savefig("{} nums of pose.jpg".format(city))
    plt.close()

def city_pose_share():
    for i in city:
        city_pose_rec(i)

def pose_compare(pose1,pose2):
    """
    不同职位的在不同城市的招聘量对比
    :param pose1:
    :param pose2:
    :return:
    """
    plt.figure(figsize=(15, 6), dpi=200, frameon=False)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    labels = city
    v1 = []
    v2 = []
    for c in city:
        v1.append(coll.count({"city":c,"pose_type":pose1}))
        v2.append(coll.count({"city":c,"pose_type":pose2}))
    x = list(range(len(v1)))
    total_width,n = 0.5,2
    width = total_width/n
    plt.bar(x,v1,width=width,label=pose1,color=colors[2])
    for i in range(len(x)):
        x[i] = x[i]+width+0.01
    plt.bar(x,v2,width=width,label = pose2,tick_label = labels,color=colors[3])
    plt.title("compare of {} and {}".format(pose1,pose2), loc="left", fontsize=15, fontweight="medium")
    plt.legend()
    plt.savefig("compare of {} and {}.jpg".format(pose1,pose2))
    plt.close()

def pose_compare_graph():
    """每个职位和Python进行不同城市下的招聘量对比"""
    select_pose = ['.net','ruby', 'go', 'java','c', 'c#','node.js', 'perl', 'c++','delphi', 'vb', 'php']
    for i in select_pose:
        pose_compare("python",i)

def edu_compare(pose):
    """
    :param pose:职位类型
    :return: 特定职位下的对学历的要求的占比，用饼图绘制出
    """
    edu_label = ["本科","大专","硕士","不限","博士"]
    data = dict.fromkeys(edu_label)
    for e in edu_label:
        data[e] = coll.count({"pose_type":pose,"edu":e})
    labels = list(data.keys())
    values = list(data.values())
    plt.title(pose, loc="left", fontsize=17, fontweight="medium")
    plt.rcParams['font.sans-serif'] = ['SimHei']
    explode = [0.05 for _ in range(len(data))]
    plt.pie(values, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=50)
    plt.axis('equal')
    plt.savefig("edu compare of {}.jpg".format(pose))
    plt.close()

def edu_pose_pie():
    for i in pose:
        edu_compare(i)

def pose_edu_com(edu):
    """
    :param edu: 学历
    :return: 特定学历下的职位类型招聘数量对比，用条形图绘制
    """
    pose_lst = ['oracle', '.net', '自然语言处理', '深度学习', '图像处理', 'ios', '语音识别', 'ruby',\
        '自动化测试', 'go', 'java', '搜索算法', 'c', 'c#', '机器学习', '测试工程师', \
        'node.js', 'web前段', '算法工程师', 'web前端', 'python', 'c++', '区块链', 'hadoop', '图像识别', 'mysql', '数据挖掘', '机器视觉', '运维工程师', 'php', 'android'
]
    data = dict.fromkeys(pose_lst)
    for i in pose_lst:
        data[i] = coll.count({"pose_type":i,"edu":edu})/coll.count({"pose_type":i})
    data_ = sorted(data.items(), key=lambda d: d[1], reverse=True)
    x_data,y_data = [i[0] for i in data_],[i[1] for i in data_]
    plt.figure(figsize=(15, 6), dpi=200, frameon=False)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    x = range(len(y_data))
    color = random.choice(colors)
    rec_gr = plt.bar(x=x_data, height=y_data, width=0.1, alpha=0.8, color=color, label=pose)
    plt.ylim()
    plt.ylabel("ratio", size=18)
    plt.xlim()
    plt.xticks(rotation=70)
    plt.xlabel("pose", size=18)
    plt.title(edu, loc="right", fontsize=17, fontweight="medium")
    plt.savefig("{} nums of pose.jpg".format(edu))
    plt.close()

def edu_pose_rank():
    edu_label = ["本科", "大专", "硕士", "不限", "博士"]
    for i in edu_label:
        pose_edu_com(i)

def salary_rank():
    """
    平均薪酬的排名
    :return:
    """
    data = dict.fromkeys(pose)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    for i in pose:
        counts = coll.count({"pose_type":i})
        s = []
        for j in coll.find({"pose_type":i}):
            if j["salary"][1] == None:
                s.append(j["salary"][0])
            else:
                s.append((j["salary"][0]+j["salary"][1])/2)
        total = sum(s)
        data[i] = total/counts
    data_ = sorted(data.items(), key=lambda d: d[1], reverse=True)
    x_data, y_data = [i[0] for i in data_], [i[1] for i in data_]
    plt.figure(figsize=(15, 6), dpi=200, frameon=False)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    x = range(len(y_data))
    color = random.choice(colors)
    rec_gr = plt.bar(x=x_data, height=y_data, width=0.1, alpha=0.8, color=color, label=pose)
    plt.ylim()
    plt.ylabel("ratio", size=18)
    plt.xlim()
    plt.xticks(rotation=70)
    plt.xlabel("pose", size=18)
    plt.title("AVG rank", loc="right", fontsize=17, fontweight="medium")
    plt.savefig("AVG_RANK.jpg")
    plt.close()

def fina_to_pose(pose):
    """
    :param pose:职位
    :return: 特定职位下的招聘公司的融资状况
    """
    data = {}
    fin_stage = ["不需要融资","未融资","上市公司","B轮","A轮","天使轮","C轮","D轮及以上"]
    for i in fin_stage:
        data[i] = coll.count({"pose_type":pose,"financeStage":i})
    # plt.figure(figsize=(5, 5), dpi=200, frameon=False)
    data_ = sorted(data.items(), key=lambda d: d[1], reverse=True)
    x_data, y_data = [i[0] for i in data_], [i[1] for i in data_]
    plt.rcParams['font.sans-serif'] = ['SimHei']
    label = x_data
    value = y_data
    x = range(len(value))
    color = random.choice(colors)
    rec_gr = plt.bar(x=label, height=value, width=0.2, alpha=0.8, color=color, label=pose)
    plt.ylim()
    plt.ylabel("nums", size=12)
    plt.xlim()
    plt.xticks(rotation=20)
    plt.xlabel("finance stage", size=12)
    plt.title("company finance stage of {} ".format(pose), loc="right", fontsize=10, fontweight="medium")
    plt.savefig("finance stage of {}.jpg".format(pose))
    plt.close()

def fine_to_pose_graph():
    for i in pose:
        fina_to_pose(i)

def pose_to_fin(fin_stage):
    """
    :param fin_stage: 融资状况
    :return: 得到特定融资状况的公司，对不同职位需求的数据对比
    """
    plt.figure(figsize=(15, 6), dpi=200, frameon=False)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    data = {}
    for c in pose:
        data[c] = coll.count({"pose_type": c, "financeStage": fin_stage})/coll.count({"pose_type": c})
    data_ = sorted(data.items(), key=lambda d: d[1], reverse=True)
    x_data, y_data = [i[0] for i in data_], [i[1] for i in data_]
    label = x_data
    value = y_data
    x = range(len(value))
    color = random.choice(colors)
    rec_gr = plt.bar(x=label, height=value, width=0.1, alpha=0.8, color=color, label=pose)
    plt.ylim()
    plt.ylabel("ratio", size=18)
    plt.xlim()
    plt.xticks(rotation=70)
    plt.xlabel("pose", size=18)
    plt.title("rank of {}".format(fin_stage), loc="right", fontsize=17, fontweight="medium")
    plt.savefig("pose of finance stage of {}.jpg".format(fin_stage))
    plt.close()

def fin_rank():
    fin_lst = ["不需要融资", "未融资", "上市公司", "B轮", "A轮", "天使轮", "C轮", "D轮及以上"]
    for i in fin_lst:
        pose_to_fin(i)

if __name__ == '__main__':
    city_big_share()
    city_pose_share()
    pose_compare_graph()
    edu_pose_pie()
    edu_pose_rank()
    salary_rank()
    fine_to_pose_graph()
    fin_rank()






