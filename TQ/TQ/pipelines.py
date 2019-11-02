# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

from pymongo import MongoClient
class TqPipeline(object):
    def open_spider(self, spider):
        self.conn = MongoClient("localhost", 27017)

    def process_item(self, item, spider):
        db = self.conn["atmosphere"]
        city=item["city"]
        collection = db[city]
        collection.insert(dict(item))
        return item