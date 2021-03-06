from redis  import StrictRedis
tasks = [
            "https://www.renrenche.com/cn/DS/",#DS
            "https://www.renrenche.com/cn/Jeep/",#Jeep
            "https://www.renrenche.com/cn/aodi/",#奥迪
            "https://www.renrenche.com/cn/baoma/",#宝马
            "https://www.renrenche.com/cn/benchi/",#奔驰
            "https://www.renrenche.com/cn/bentian/",#本田
            "https://www.renrenche.com/cn/biaozhi/",#标志
            "https://www.renrenche.com/cn/bieke/",#别克
            "https://www.renrenche.com/cn/dazhong/",#大众
            "https://www.renrenche.com/cn/fengtian/",#丰田
            "https://www.renrenche.com/cn/fute/",#福特
            "https://www.renrenche.com/cn/jiebao/",#捷豹
            "https://www.renrenche.com/cn/kaidilake/",#凯迪拉克
            "https://www.renrenche.com/cn/leikesasi/",#雷克萨斯
            "https://www.renrenche.com/cn/luhu/",#路虎
            "https://www.renrenche.com/cn/mazida/",#马自达
            "https://www.renrenche.com/cn/richan/",#日产
            "https://www.renrenche.com/cn/woerwo/",#沃尔沃
            "https://www.renrenche.com/cn/wulingqiche/",#五菱
            "https://www.renrenche.com/cn/xiandai/",#现代
            "https://www.renrenche.com/cn/xuefolan/",#雪佛兰
            "https://www.renrenche.com/cn/xuetielong/",#雪铁龙
            "https://www.renrenche.com/cn/yingfeinidi/"#英菲尼迪
        ]

r = StrictRedis()
for i in tasks:
    r.lpush("RRC:start_urls",i)