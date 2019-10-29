# -*- coding: utf-8 -*-
import time

import scrapy
import json
from ..items import DouyunItem


class DySpider(scrapy.Spider):
    name = 'dy'
    allowed_domains = ['www.douyu.com', "rpic.douyucdn.cn"]
    start_urls = ['https://www.douyu.com/gapi/rknc/directory/yzRec/1']

    def parse(self, response):
        data = json.loads(response.body)
        for each in data['data']['rl']:
            item = DouyunItem()
            item["img"] = each['rs16']
            item["name"] = each['nn']
            yield item

