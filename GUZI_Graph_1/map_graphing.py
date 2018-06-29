from pyecharts import Geo
import pymongo
client = pymongo.MongoClient()
db = client["GUAZI"]
coll = db["cleaned_data"]
car_ = ["Jeep","奥迪","宝马","保时捷","奔驰","比亚迪","别克","大众","法拉利","丰田","福特","捷豹","凯迪拉克","雷克萨斯","路虎","马自达","玛莎拉蒂","日产","斯巴鲁","特斯拉",\
        "沃尔沃","五菱","现代","雪佛兰","雪铁龙","英菲尼迪","众泰"]
def car_city(brand):
    """

    :param brand:汽车品牌
    :return:得到某个品牌的在不同城市的数量
    """
    data = []
    city_lst = set()
    for i in coll.find({"car":brand}):
        city_lst.add(i["city"])
    city_lst.remove("广安")
    city_lst.remove("眉山")
    city_lst.remove("达州")
    city_lst = list(city_lst)
    for c in city_lst:
        data.append((c,coll.count({"car":brand,"city":c})))
    return data
def geo_graph(brand):
    """
    热力图绘制
    :param brand: 汽车品牌
    :return:
    """
    data = car_city(brand)
    geo = Geo(brand, brand+"distribution", title_color="#fff",
              title_pos="center", width=1200,
              height=600, background_color='#404a59')
    attr, value = geo.cast(data)
    geo.add("", attr, value, visual_range=[0, 200], visual_text_color="#fff",
            symbol_size=15, is_visualmap=True)
    geo.render()

if __name__ == '__main__':
    # geo_graph('Jeep')
    # geo_graph('奥迪')
    # geo_graph('宝马')
    # geo_graph('保时捷')
    # geo_graph('奔驰')
    # geo_graph('比亚迪')
    # geo_graph('别克')
    # geo_graph('大众')
    # geo_graph('法拉利')
    # geo_graph('丰田')
    # geo_graph('福特')
    # geo_graph('捷豹')
    # geo_graph('凯迪拉克')
    # geo_graph('雷克萨斯')
    # geo_graph('路虎')
    # geo_graph('马自达')
    # geo_graph('玛莎拉蒂')
    # geo_graph('日产')
    # geo_graph('斯巴鲁')
    # geo_graph('特斯拉')
    # geo_graph('沃尔沃')
    # geo_graph('五菱')
    # geo_graph('现代')
    # geo_graph('雪佛兰')
    # geo_graph('雪铁龙')
    # geo_graph('英菲尼迪')
    geo_graph('众泰')

