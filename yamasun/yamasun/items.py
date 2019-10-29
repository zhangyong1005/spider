# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YamasunItem(scrapy.Item):
    name=scrapy.Field()
    author=scrapy.Field()
    type=scrapy.Field()
    price=scrapy.Field()
    first_type=scrapy.Field()
    two_type=scrapy.Field()
