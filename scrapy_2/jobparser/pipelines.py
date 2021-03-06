# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import numpy as np


class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancies_2
        self.adjustments = JobparserItemAdjustmentsPipeline()

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        item = self.adjustments.item_adjustments(item, spider)
        collection.insert_one(item)
        return item


class JobparserItemAdjustmentsPipeline(object):
    def item_adjustments(self, item, spider):
        item['min_salary'] = np.nan
        item['max_salary'] = np.nan
        item['currency'] = np.nan
        if spider.name == 'sj':
            item = self.sj_item_adjustments(item)
        elif spider.name == 'hhru':
            item = self.hhru_item_adjustments(item)
        return item

    def sj_item_adjustments(self, item):
        item['site'] = 'https://russia.superjob.ru'
        if len(item['salary']) >= 2:
            if item['salary'][0] == "от":
                item['min_salary'] = int(item['salary'][2][:-4].replace('\xa0', '').replace(' ', ''))
                item['currency'] = item['salary'][2][-4:]
            elif item['salary'][0].replace('\xa0', '').replace(' ', '').isnumeric():
                item['min_salary'] = int(item['salary'][0].replace('\xa0', '').replace(' ', ''))
                item['max_salary'] = int(item['salary'][1].replace('\xa0', '').replace(' ', ''))
                item['currency'] = item['salary'][3]
        return item

    def hhru_item_adjustments(self, item):
        item['site'] = 'https://hh.ru/'
        if len(item['salary']) != 0:
            for i in range(len(item['salary'])):
                if item['salary'][i] == "от ":
                    item['min_salary'] = int(item['salary'][i + 1].replace('\xa0', '').replace(' ', ''))
                elif (item['salary'][i] == " до ") | (item['salary'][i] == "до "):
                    item['max_salary'] = int(item['salary'][i + 1].replace('\xa0', '').replace(' ', ''))
                elif (item['salary'][i] == "руб.") | (item['salary'][i] == "USD") | (item['salary'][i] == "EUR"):
                    item['currency'] = item['salary'][i]
        return item











