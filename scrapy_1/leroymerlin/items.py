# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose
import re


def cleaner_photo(values):
    if values[:2] == '//':
        return f'http:{values}'
    return values


def cleaner_price(values):
    return int(values.replace(' ', ''))


def cleaner_specification(values):
    pattern = re.compile('[\w\(\),\.\+\/.]+')
    return (' '.join(pattern.findall(values)))


class LeroymerlinItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))
    price = scrapy.Field(input_processor=MapCompose(cleaner_price), output_processor=TakeFirst())
    s_keys = scrapy.Field()
    s_values = scrapy.Field(input_processor=MapCompose(cleaner_specification))
    specification = scrapy.Field()

