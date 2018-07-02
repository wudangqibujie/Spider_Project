import pymongo
import datetime
import random
import matplotlib.pyplot as plt
client = pymongo.MongoClient()
db = client["LJ_Spider"]
city_lst =[ 'guangzhou', 'zhongshan', 'beijing', 'dongguan', 'foshan', 'shanghai', 'zhuhai', 'shenzhen', 'huizhou']
coll = db["shanghai"]
colors = ["dimgray", "orange", "lightgreen", "cornflowerblue", "sandybrown", "cadetblue", "darkkhaki", "coral",\
       "burlywood", "wheat", "lightsteelblue", "mediumaquamarine", "plum", "tomato", "skyblue", "gold", "c",\
       "powderblue", "darksalmon"]
# for i in coll.find():
#     print(i)
# a = datetime.datetime.strptime('2001','%Y')
# print(a)
def scatter_graph(x_data,y_data,title,x_label,y_label,c):
    fig = plt.figure(figsize = (9.5,7.5),dpi=200,frameon=False)
    ax1 = fig.add_subplot(111)
    ax1.set_title(title,loc="right", fontsize=13, fontweight="medium")
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # plt.xlim(datetime(2005, 1, 1, 0, 0), datetime(2018, 3, 1, 0, 0))
    # plt.ylim(0, y_lim)
    plt.xlabel(x_label,size=12)
    plt.ylabel(y_label,size=12)
    ax1.scatter(x_data,y_data,c=c, marker='o', s=0.5)
    plt.savefig("{}.jpg".format(title+" "))
    plt.close()
def get_data(city):
    x_data,y_data = [],[]
    for i in db[city].find():
        if i["year"] != "null":
            x_data.append(datetime.datetime.strptime(str(i["year"]),'%Y'))
            y_data.append(i["uni_price"])
    c = random.choice(colors)
    scatter_graph(x_data,y_data,city.title()+" uniprice of year","Year","Uni price",c)
def year_uin():
    for i in city_lst:
        get_data(i)
def bar_graph(x_data,y_data,title_name,file_name,color,x_label,y_label,x_l_lim = None,x_h_lim=None,y_l_lim = None,y_h_lim = None):
    plt.figure(figsize=(15, 6), dpi=200, frameon=False)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    x_ = range(len(y_data))
    rec_gr = plt.bar(x=x_data,height = y_data,width = 0.2,color = color,label = "A")
    plt.ylim(y_l_lim,y_h_lim)
    plt.xlim(x_l_lim,x_h_lim)
    plt.xlabel(x_label,size = 18,)
    plt.ylabel(y_label,size = 18)
    plt.xticks()
    plt.xticks(rotation=0)
    plt.title(title_name,loc = "right",fontsize = 17,fontweight = "medium")
    plt.savefig("{}.jpg".format(file_name))
    plt.close()
def year_ratio(city):
    year = set()
    for i in db[city].find():
        year.add(i["year"])
    data = {}
    for j in list(year):
        data[j] = db[city].count({"year":j})
    return data
def year_graph(city):
    data = year_ratio(city)
    sorted(data.items(), key=lambda e: e[1], reverse=False)
    del data["null"]
    x_data,y_data = list(data.keys()),list(data.values())
    bar_graph(x_data,y_data,city.title(),city+" year",random.choice(colors),"Year","Nums")
def sty_graph(city):
    lst = ["{}室".format(i) for i in range(1,7)]
    data = dict.fromkeys(lst)
    for i in lst:
        data[i] = db[city].count({"sty":{"$regex":i}})
    data = sorted(data.items(), key=lambda d: d[1], reverse=True)
    x_data, y_data = [i[0] for i in data], [i[1] for i in data]
    bar_graph(x_data,y_data,city.title(),city+" style",random.choice(colors),"Style","Nums")
def all_sty():
    for i in city_lst:
        sty_graph(i)
def city_sty(sty):
    data = dict.fromkeys(city_lst,0)
    for i in city_lst:
        sum_ = db[i].count()
        data[i] = db[i].count({"sty":{"$regex":sty}})/sum_
    data = sorted(data.items(), key=lambda d: d[1], reverse=True)
    x_data, y_data = [i[0] for i in data], [i[1] for i in data]
    bar_graph(x_data, y_data, sty.title(), sty + " city", random.choice(colors), "city", "Nums")
def all_city_sty():
    lst = ["{}室".format(i) for i in range(1, 10)]
    for i in lst:
        city_sty(i)
if __name__ == '__main__':
    # get_data("shenzhen")
    # year_uin()
    # year_ratio("shanghai")
    # year_graph("shanghai")
    # year_graph("beijing")
    # year_graph("dongguan")
    # year_graph("foshan")
    # year_graph("zhongshan")
    # all_sty()
    all_city_sty()