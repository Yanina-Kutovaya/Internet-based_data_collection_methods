# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import os
from urllib.parse import urlparse
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from pymongo import MongoClient


class LeroymerlinPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroymernin

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        item['specification'] = dict(zip(item['s_keys'], item['s_values']))
        item.pop('s_keys')
        item.pop('s_values')
        collection.insert_one(item)
        return item


class LeroymerlinImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        file_name = os.path.basename(urlparse(request.url).path)
        path = os.getcwd() + '\images'
        product_list = [x[0] for x in os.walk(path)]
        for i in product_list:
            if i[-8:] == file_name[:8]:
                product = i.split('\\')[-1]
                return f'{product}/{file_name}'

    def get_media_requests(self, item, info):
        s = 'images/' + item['link'].split('/')[-2].replace('-', '_')
        os.mkdir(s)
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item
