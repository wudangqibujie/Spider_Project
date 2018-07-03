import pymongo
import time
import datetime
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
import jieba
from PIL import Image

colors = ["dimgray", "orange", "lightgreen", "cornflowerblue", "sandybrown", "cadetblue", "darkkhaki", "coral",\
       "burlywood", "wheat", "lightsteelblue", "mediumaquamarine", "plum", "tomato", "skyblue", "gold", "c",\
       "powderblue", "darksalmon"]
client = pymongo.MongoClient()
db = client["ICE_DATA"]
def get_ICE_arti_data():
    data = {}
    for i in db["data"].find():
        a = i["target"]
        try:
            author = a["author"]
            if "数据冰山" in author["name"]:
                data["title"] = a["title"]
                data["id"] = a["id"]
                data["voted_nums"] = a["voteup_count"]
                data["comment+nums"] = a["comment_count"]
                data["post_time_c"] = a["created"]
                data["man_time"] = datetime.datetime.fromtimestamp(a["created"])
                yield data
        except Exception as e:
            pass
def bar_graph(x_data,y_data,title_name,file_name,color,x_label,y_label,x_l_lim = None,x_h_lim=None,y_l_lim = None,y_h_lim = None):
    plt.figure(figsize=(8, 4), dpi=200, frameon=False)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    x_ = range(len(y_data))
    rec_gr = plt.bar(x=x_data,height = y_data,width = 1,color = color)
    plt.xlabel(x_label,size = 8)
    plt.ylabel(y_label,size = 8)
    plt.xticks(rotation=0,size=6)
    plt.yticks(size=6)
    plt.title(title_name,loc = "right",fontsize = 7,fontweight = "medium")
    plt.savefig("{}.jpg".format(file_name))
    plt.close()
def show_graph():
    x_data,comm_data,vot_data = [],[],[]
    for i in get_ICE_arti_data():
        print(i)
        x_data.append(i["man_time"])
        comm_data.append(i["comment+nums"])
        vot_data.append(i["voted_nums"])
    bar_graph(x_data,comm_data,"ICE Article comment counts thrend","ICE DATA COMM",colors[5],"Time","Comment Counts")
    bar_graph(x_data, vot_data, "ICE Article voted counts thrend", "ICE DATA VOTED", colors[7], "Time","Voted Counts")
def comment():
    day_set = set()
    day_data = dict()
    x_data,y_data = [],[]
    for i in db["comment_lst"].find():
        day_set.add(i["day"])
    for j in list(day_set):
        day_data[j] = db["comment_lst"].count({"day":j})
    for k in day_data.keys():
        x_data.append(datetime.datetime.strptime(k,'%Y-%m-%d'))
        y_data.append(day_data[k])
    return x_data,y_data
def comment_2():
    day_set = set()
    day_data = dict()
    x_data,y_data = [],[]
    for i in db["comment_lst"].find():
        day_set.add(i["month"])
    for j in list(day_set):
        day_data[j] = db["comment_lst"].count({"month":j})
    for k in day_data.keys():
        x_data.append(datetime.datetime.strptime(k,'%Y-%m'))
        y_data.append(day_data[k])
    return x_data,y_data
def comment_graph():
    x_data,y_data = comment()
    bar_graph(x_data,y_data,"Comment Trend Day","Comment ICE Day",colors[1],"Time","Comment Counts")
    x1_data,y1_data = comment_2()
    bar_graph(x1_data, y1_data, "Comment Trend Month", "Comment ICE Month", colors[7], "Time", "Comment Counts")
def gender_ratio():
    data = {"男":None,"女":None,"不明性别":None}
    # for i in db["comment_lst"].find():
    data["男"] = db["comment_lst"].count({"author.member.gender":1})
    data["女"] = db["comment_lst"].count({"author.member.gender":0})
    data["不明性别"] = db["comment_lst"].count({"author.member.gender":-1})
    return data
def pie_graph(obj,colors,filename,title):
    # plt.figure( dpi=600, frameon=False)
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
    pie_graph(gender_ratio(),colors[2:7],"Gender Ratio","Gender Ratio")
def comment_cloud():
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
def headline_cloud():
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
def user_gender():
    data = {"男": None, "女": None, "不明性别": None}
    data["男"] = db["user_info"].count({"gender": 1})
    data["女"] = db["user_info"].count({"gender": 0})
    data["不明性别"] = db["user_info"].count({"gender": -1})
    return data
def user_gender_graph():
    pie_graph(user_gender(), colors[2:7], "User Gender Ratio", "User Gender Ratio")
if __name__ == '__main__':
    # show_graph()
    # comment_graph()
    # gender_graph()
    # comment_cloud()
    # user_cloud()
    # headline_cloud()
    user_gender_graph()
    pass



    # d1 = datetime.datetime.strptime('2017-10-18 00:00:00', '%Y-%m-%d %H:%M:%S').timetuple()
    # d2 = datetime.datetime.strptime('2017-10-19 00:00:00', '%Y-%m-%d %H:%M:%S').timetuple()
    # aa = time.mktime(d2)-time.mktime(d1)
    # print(aa)


