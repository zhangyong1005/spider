# -*- coding: utf-8 -*-
import scrapy

from ..items import TqItem
from scrapy_redis.spiders import RedisSpider
class TqSpider(RedisSpider):
    name = 'tq'
    allowed_domains = ['aqistudy.cn']
    base_url = "https://www.aqistudy.cn/historydata/"
    redis_key = 'redis_key:urls'

    def parse(self, response):
        print("正在爬取城市信息")
        Url_list = response.xpath('//div[@class="all"]/div[@class="bottom"]//a/@href').extract()
        city_list = response.xpath('//div[@class="all"]/div[@class="bottom"]//a/text()').extract()
        for Url, city in zip(Url_list, city_list):
            link = self.base_url + Url
            yield scrapy.Request(url=link, callback=self.parse_mouth, meta={"city": city})

    def parse_mouth(self, response):
        print("正在爬取城市月份")

        Url_list = response.xpath('//tr/td/a/@href').extract()

        for Url in Url_list:
            link = self.base_url + Url
            print(link)
            yield scrapy.Request(url=link, callback=self.parse_day, meta={"city": response.meta['city']})

    def parse_day(self, response):
        print("正在爬取最终数据")
        node_list = response.xpath('//tr')
        node_list.pop(0)

        for node in node_list:
            item = TqItem()
            item['city'] = response.meta['city']
            item['date'] = node.xpath('./td[1]/text()').extract_first()
            item['aqi'] = node.xpath('./td[2]/text()').extract_first()
            item['level'] = node.xpath('./td[3]//text()').extract_first()
            item['pm2_5'] = node.xpath('./td[4]/text()').extract_first()
            item['pm10'] = node.xpath('./td[5]/text()').extract_first()
            item['so2'] = node.xpath('./td[6]/text()').extract_first()
            item['co'] = node.xpath('./td[7]/text()').extract_first()
            item['no2'] = node.xpath('./td[8]/text()').extract_first()
            item['o3'] = node.xpath('./td[9]/text()').extract_first()
            yield item
