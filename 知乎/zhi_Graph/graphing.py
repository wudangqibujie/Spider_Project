import pymongo
import time
import datetime
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
import jieba
import random
from PIL import Image
client = pymongo.MongoClient()
db = client["BINSHAN"]
colors = ["dimgray", "orange", "lightgreen", "cornflowerblue", "sandybrown", "cadetblue", "darkkhaki", "coral",\
       "burlywood", "wheat", "lightsteelblue", "mediumaquamarine", "plum", "tomato", "skyblue", "gold", "c",\
       "powderblue", "darksalmon"]
def bar_graph(x_data,y_data,title_name,file_name,color,x_label,y_label,x_l_lim = None,x_h_lim=None,y_l_lim = None,y_h_lim = None):
    """条形图"""
    plt.figure(figsize=(8, 4), dpi=200, frameon=False)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    x_ = range(len(y_data))
    rec_gr = plt.bar(x=x_data,height = y_data,width = 0.4,color = color)
    plt.xlabel(x_label,size = 8)
    plt.ylabel(y_label,size = 8)
    plt.xticks(rotation=0,size=6)
    plt.yticks(size=6)
    plt.title(title_name,loc = "right",fontsize = 7,fontweight = "medium")
    plt.savefig("{}.jpg".format(file_name))
    plt.close()
def data_graph(item):
    """
    :param item: 评论数/点赞数
    :return: 生成时间序列上的文章点赞数/评论数条形图
    """
    x_data,y_data = [],[]
    for i in db["arti_info"].find():
        x_data.append(time_pro(i["created"]))
        y_data.append(i[item])
    bar_graph(x_data,y_data,item.title()+" trend",item,random.choice(colors),"Time",item)
        # print(i["title"],i["voteup_count"],i["comment_count"],i["created"])
def time_pro(raw_time):
    """
    :param raw_time:时间戳
    :return: 格式化成datetime
    """
    time_local = time.localtime(raw_time)
    dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
    new = datetime.datetime.strptime(dt,"%Y-%m-%d %H:%M:%S")
    return new
def gender_ratio():
    """
    :return:返回关注用户的性别
    """
    data = {"男":None,"女":None,"不明性别":None}
    # data["男"] = db["comm_detail"].count({"author.member.gender":1})
    # data["女"] = db["comm_detail"].count({"author.member.gender":0})
    # data["不明性别"] = db["comm_detail"].count({"author.member.gender":-1})
    data["男"] = db["user_detail"].count({"gender": 1})
    data["女"] = db["user_detail"].count({"gender": 0})
    data["不明性别"] = db["user_detail"].count({"gender": -1})
    print(data)
    return data
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
def gender_graph():
    """生成关注用户数的男女比例的饼图"""
    pie_graph(gender_ratio(),colors[2:7],"Gender Ratio Of Follewer","Gender Ratio Of Follower")
    # pie_graph(gender_ratio(),colors[2:7],"Gender Ratio Of commer","Gender Ratio Of commer")

def follower_loc():
    """关注用户所处的城市"""
    loc = set()
    sum = 0
    for i in db["user_detail"].find():
        if "location" in i.keys():
            ci = i["location"][0]["name"]
            loc.add(ci)
    data = dict()
    print(len(loc))
    for c in list(loc):
        sum+=1
        print(sum)
        data[c] = db["user_detail"].count({"location.0.name":c})
    print(data)
    data["广州"] = data["广州"]+data["广州市"]
    del data["广州市"]
    data_ = sorted(data.items(), key=lambda d: d[1], reverse=True)
    x_data, y_data = [i[0] for i in data_], [i[1] for i in data_]
    bar_graph(x_data[:20],y_data[:20],"Location Distribution of Follower","Location Distribution of Follower","gold","Place","Nums")
def headline_cloud():
    """生成关注用户签名的云图"""
    a = []
    f = open('headline.txt', 'r', encoding="utf-8").read()
    words = list(jieba.cut(f))
    for word in words:
        if len(word) > 1:
            a.append(word)
    txt = r' '.join(a)
    wordcloud = WordCloud(background_color="white", font_path='WE.TTF', width=1000, height=860,
                          margin=2).generate(txt)
    wordcloud.to_file("Headline.jpg")
def comment_cloud():
    """生成文章评论的云图"""
    a = []
    f = open('comment.txt', 'r', encoding="utf-8").read()
    words = list(jieba.cut(f))
    for word in words:
        if len(word) > 1:
            a.append(word)
    txt = r' '.join(a)
    wordcloud = WordCloud(background_color="white", font_path='WE.TTF', width=1000, height=860,
                          margin=2).generate(txt)
    wordcloud.to_file("Comment Cloud.jpg")
def user_cloud():
    """生成用户的教育背景云图"""
    a = []
    f = open('user edu.txt', 'r', encoding="utf-8").read()
    words = list(jieba.cut(f))
    for word in words:
        if len(word) > 1:
            a.append(word)
    txt = r' '.join(a)
    wordcloud = WordCloud(background_color="white", font_path='WE.TTF', width=1000, height=860,
                          margin=2).generate(txt)
    wordcloud.to_file("User Edu.jpg")

if __name__ == '__main__':
    data_graph("voteup_count")
    data_graph("comment_count")
    gender_graph()
    follower_loc()
    headline_cloud()
    comment_cloud()
    user_cloud()
    # f = open("user edu.txt","w",encoding="utf-8")
    # for i in db["user_detail"].find():
    #     if "education" in i.keys():
    #         aa = i["education"][0]["name"]
    #         if aa:
    #             f.write(aa+"\n")