# -*- coding: utf-8 -*-
import time

import scrapy
from ..items import YamasunItem
from scrapy_redis.spiders import RedisSpider


class AmazonSpider(RedisSpider):

    name = 'amazon'
    allowed_domains = ['amazon.cn']
    base_url = "https://www.amazon.cn"
    # start_urls = ['https://www.amazon.cn/%E5%9B%BE%E4%B9%A6/b/ref=sd_allcat_books_I1?ie=UTF8&node=658390051']
    redis_key="amazon:url"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36",
        "Cookie": {
            "x-wl-uid": "1KuyLpTbhDjUf3r73ETeKIBSp4Oh2OfxNzt3vRQtpGkZWqnc3PqNefSpKf9aVrfDuehwwCfLme0U=",
            "session-id": "457-6570365-0189511",
            "ubid-acbcn": "457-3814021-6405549",
            "session-token": "aDjfQvoEBxfq43RxjRtv3vgj857HsxojcrsHU81y54likrs4w7qFPIbfztQBDX4vrUMGTfSOOzFDAfzo3YoSQQWOxzqmFKYdovx+CN+1TKNvEopR2+quT9dAROaNqR/p+UNZkzIIGlc0lAiH5msU7JhwFE8PgHfeHij5n5xHm7OaVPRSfNLNX6557kfRee2i",
            "session-id-time": "2082729601l",
            "csm-hit": "tb:D8HVWS6DTNZ8ADAF7CET+s-YRKW74KZ61Q0YFKPV9A6|1571653565529&t:1571653565529&adb:adblk_yes",
        },
    }
    def parse(self, response):
        url_list = response.xpath(
            '//ul[@class="a-unordered-list a-nostyle a-vertical s-ref-indent-one"]//a/@href').extract()
        type_list = response.xpath(
            '//ul[@class="a-unordered-list a-nostyle a-vertical s-ref-indent-one"]//a/span/text()').extract()
        for Url, type in zip(url_list, type_list):
            yield scrapy.Request(url=Url, callback=self.parse_type, meta={"first_type": type},headers=self.headers)

    def parse_type(self, response):
        first_type = response.meta["first_type"]
        url_list = response.xpath(
            '//ul[@class="a-unordered-list a-nostyle a-vertical s-ref-indent-two"]//a/@href').extract()
        type_list = response.xpath(
            '//ul[@class="a-unordered-list a-nostyle a-vertical s-ref-indent-two"]//a/span/text()').extract()
        for Url, type in zip(url_list, type_list):
            yield scrapy.Request(url=Url, callback=self.parse_info, meta={"first_type": first_type, "two_type": type},headers=self.headers)

    def parse_info(self, response):
        #该类书的第一页
        first_type = response.meta["first_type"]
        two_type = response.meta["two_type"]
        item = YamasunItem()
        node_list = response.xpath(
            '//ul[@class="s-result-list s-col-1 s-col-ws-1 s-result-list-hgrid s-height-equalized s-list-view s-text-condensed s-item-container-height-auto"]/li')

        for node in node_list:
            #书名
            item["name"] = node.xpath('.//a/h2/text()').extract_first()
            #作者
            item["author"] = node.xpath(
                './/div[@class="a-fixed-left-grid-col a-col-right"]//div/span[@class="a-size-small a-color-secondary"][2]/text()').extract_first()
            #书的销售类型
            item["type"] = node.xpath('.//a/h3/text()').extract_first()
            #书的价格
            item["price"] = node.xpath('.//a/span[2]/text()').extract_first()
            #书的最外层的分类
            item["first_type"]=first_type
            #书的外层分类的具体类别
            item["two_type"]=two_type
            yield item
        next_url = self.base_url + response.xpath('//span[@class="pagnRA"]/a/@href').extract_first()
        print(next_url)
        if next_url:
            time.sleep(0.5)
            yield scrapy.Request(url=next_url, callback=self.parse_next,meta={"first_type": first_type, "two_type": two_type},headers=self.headers)

    def parse_next(self, response):
        #第一页跟后面的页数页面结构不一样
        first_type = response.meta["first_type"]
        two_type = response.meta["two_type"]
        item = YamasunItem()
        node_list = response.xpath(
            '//div[@class="s-result-list s-search-results sg-row"]/div/div/span/div/div/div[2]/div[2]')
        for node in node_list:
            item["name"] = node.xpath('.//h2/a/span/text()').extract_first()
            item["author"] = node.xpath('.//div[@class="a-section a-spacing-none"]/div/span[2]/text()').extract_first()
            item["type"] = node.xpath('./div/div[2]/div/div/div/div/a/text()').extract_first().strip()
            item["price"] = node.xpath('./div/div[2]/div/div/div/div/div/a/span/span[1]/text()').extract_first()
            item["first_type"] = first_type
            item["two_type"] = two_type
            yield item
        try:
            next_url = self.base_url + response.xpath('//li[@class="a-last"]/a/@href').extract_first()
            time.sleep(0.5)
            yield scrapy.Request(url=next_url, callback=self.parse_next,meta={"first_type": first_type, "two_type": two_type},headers=self.headers)
        except:
            print('没有下一页了')
