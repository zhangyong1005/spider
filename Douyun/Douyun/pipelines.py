# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class DouyunPipeline(object):
    def process_item(self, item, spider):
        return item


from scrapy.pipelines.images import ImagesPipeline
import scrapy
import os
from .settings import IMAGES_STORE

class ImagePipeline(ImagesPipeline):
    IMAGES_STORE =IMAGES_STORE

    def get_media_requests(self, item, info):
        yield scrapy.Request(item['img'])

    def item_completed(self, results, item, info):
        image_path=[x['path'] for ok,x in results if ok]

        old_name=self.IMAGES_STORE+image_path[0]
        new_name=self.IMAGES_STORE+"/full/"+item['name']+'.jpg'
        os.rename(old_name,new_name)
        # item['imgpath']=self.IMAGES_STORE+"/"+item['name']
        return item