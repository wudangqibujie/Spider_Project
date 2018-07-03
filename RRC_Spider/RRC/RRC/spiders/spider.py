from scrapy import Spider,Request
from scrapy_redis.spiders import RedisSpider
from RRC.items import Infotem,ReportItem
from urllib.parse import urljoin
class EECSpider(RedisSpider):
    name = "RRC"
    redis_key = "RRC:start_urls"
    base_url = "https://www.renrenche.com/"
    def parse(self, response):
        base_link = response.meta.get("base_link") if response.meta.get("base_link") else response.url
        next_page = response.meta.get("now_page")+1  if response.meta.get("now_page") else 2
        items = response.xpath('//ul[@class="row-fluid list-row js-car-list"]/li')
        if items:
            for i in items:
                data = Infotem()
                link = i.xpath('a/@href').extract()
                car_id = i.xpath('a/@data-car-id').extract()
                title = i.xpath('div[@class="schedule btn-base btn-wireframe"]/@data-title').extract()
                city = i.xpath('a/div[@class="img-backgound"]/div[@class="position-bg"]/span/text()').extract()
                year_age = i.xpath('a/div[@class="mileage"]/span[1]/text()').extract()
                price = i.xpath('a/div[@class="tags-box"]/div[@class="price"]/text()').extract()
                data["car_id"] = car_id
                data["title"] = title
                data["link"] = link
                data["city"] = city
                data["year_age"] = year_age
                data["price"] = price
                print(data)
                yield data
                if link:
                    detail_link = urljoin(self.base_url, link[0])
                    yield Request(detail_link,self.parse_detail,meta={"data_id": car_id})
            # base_link = response.url
            # next_page = response["now_page"] + 1
            next_link = base_link + "p" + str(next_page) + r"/"
            print(next_link)
            yield Request(next_link,self.parse,meta={"base_link": base_link, "now_page": next_page})
    def parse_detail(self,response):
        car_id = response.meta.get("data_id")
        items = response.xpath('//div[@class="other clearfixnew"]/div')
        for i in items:
            for j in i.xpath('div[@class="option"]'):
                data = ReportItem()
                data["car_id"] = car_id
                option_name = j.xpath('div[@class="child-title"]/text()').extract()
                option_counts = j.xpath('div[@class="mun"]/text()').extract()
                data["option_name"] = option_name
                data["option_counts"] = option_counts
                if j.xpath('a[@class="test-fail-box"]'):
                    fetal_counts = j.xpath('a[@class="test-fail-box"]/div[@class="test-fail"]/div[@class="mun"]/text()').extract()
                    data["fetal_counts"] = fetal_counts
                else:
                    fetal_counts = 0
                    data["fetal_counts"] = fetal_counts
                yield data
