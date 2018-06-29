from scrapy import Spider,Request
from scrapy_redis.spiders import RedisSpider
from urllib.parse import urljoin
from Qfang_S.items import CityItem,DetailItem
class QfangSpider(RedisSpider):
    name = "QFang"
    redis_key = "QF:start_urls"
    def parse(self, response):
        items = response.xpath('//ul[@class="cities-opts clearfix"]/li')
        for i in items:
            a_items = i.xpath('p/a[@class="highlight"]')
            if a_items:
                for j in a_items:
                    data = CityItem()
                    name = j.xpath('text()').extract()[0]
                    link = j.xpath('@href').extract()[0]
                    data["city_name"] = name
                    data["city_link"] = link
                    yield data
                    yield Request("https:" + link,self.parse_zones,meta={"city_link": link, "city_name": name})
    def parse_zones(self,response):
        base_link = response.meta.get("city_link")
        city_name = response.meta.get("city_name")
        items = response.xpath('//ul[@class="search-area-detail clearfix"]/li')[1:]
        for i in items:
            zone_ = i.xpath('a/text()').extract()
            link_ = i.xpath('a/@href').extract()
            if zone_:
                data = {}
                data["zone_name"] = zone_[0]
                data["zone_link"] = link_[0]
                yield Request("https:" + urljoin(base_link, link_[0]),self.parse_details,meta={"city_name": city_name, "zone_name": zone_[0],"zone_base_url": "https:" + urljoin(base_link, link_[0])})
    def parse_details(self, response):
        city_name = response.meta.get("city_name")
        zone_name = response.meta.get("zone_name")
        items = response.xpath('//div[@class="house-detail"]/ul/li')
        next_items = response.xpath('//div[@class="pages-box clearfix"]/div[2]/a[@class="turnpage_next"]')
        if next_items:
            if "下一页" in next_items[0].xpath('span/text()').extract()[0]:
                next_page = next_items[0].xpath('@href').extract()
                if next_page:
                    zone_base_url = response.meta.get("zone_base_url")
                    next_link = urljoin(zone_base_url, next_page[0])
                    yield Request(next_link,self.parse_details,meta = {"city_name": city_name, "zone_name": zone_name,"zone_base_url": zone_base_url})
        if items:
            for i in items:
                data = DetailItem()
                title = i.xpath('div[1]/p[@class="house-title"]/a/@title').extract()
                link = i.xpath('a/@href').extract()
                base_info = i.xpath('div[1]/p[@class="house-about clearfix"]/span/text()').extract()
                address = i.xpath('div[1]/p[@class="house-address clearfix"]/span[@class="whole-line"]/a/text()').extract()
                price = i.xpath('div[@class="show-price"]/span[@class="sale-price"]/text()').extract()
                uni_price = i.xpath('div[@class="show-price"]/p/text()').extract()
                data["title"] = title
                data["link"] = link
                data["base_info"] = base_info
                data["address"] = address
                data["price"] = price
                data["uni_price"] = uni_price
                yield data
