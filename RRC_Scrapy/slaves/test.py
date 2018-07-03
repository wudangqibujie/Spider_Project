import requests
from lxml import etree
aa = "https://www.renrenche.com/cq/car/6f5195c28e90a552?plog_id=216e09b268010808f11472c3b98f782f"
r = requests.get(aa)
html = etree.HTML(r.text)
items = html.xpath('//div[@class="other clearfixnew"]/div')
for i in items:
    for j in i.xpath('div[@class="option"]'):
        data = dict()
        option_name = j.xpath('div[@class="child-title"]/text()')
        option_counts = j.xpath('div[@class="mun"]/text()')
        data["option_name"] = option_name
        data["option_counts"] = option_counts
        if j.xpath('a[@class="test-fail-box"]'):
            fetal_counts = j.xpath('a[@class="test-fail-box"]/div[@class="test-fail"]/div[@class="mun"]/text()')
            data["fetal_counts"] = fetal_counts
        else:
            fetal_counts = 0
            data["fetal_counts"] = fetal_counts
        print(data)
