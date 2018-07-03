from pyecharts import Geo
import pymongo
import time
client = pymongo.MongoClient()
db = client["YX_F"]
coll_data = db["data"]
coll_city = db["city_id"]
car_ = ['宝马',
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

def geo_graph(brand,data):
    geo = Geo(brand, brand+"distribution", title_color="#fff",
              title_pos="center", width=1200,
              height=600, background_color='#404a59')

    attr, value = geo.cast(data)
    geo.add("", attr, value, visual_range=[0, 10000], visual_text_color="#fff",
            symbol_size=10, is_visualmap=True)
    geo.render()

def brand_map(brand):
    city_id_lst = []
    for i in coll_city.find():
        city_id_lst.append(int(i["cityid"]))
    data = []
    for j in city_id_lst:
        city_name = coll_city.find_one({"cityid": str(j)})["cityname"]
        counts = coll_data.count({"city_id": j, "title": {"$regex": brand}})
        if counts != 0:
            data.append((city_name, counts))
    print(data)
    for i in data:
        if i[0] == "达州":
            data.remove(i)
        if i[0] == "万州":
            data.remove(i)
        if i[0] == "庆阳":
            data.remove(i)
    geo_graph(brand, data)
if __name__ == '__main__':
    car = car_[23]
    brand_map(car)



