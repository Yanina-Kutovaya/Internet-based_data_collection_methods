# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    salary = scrapy.Field()
    link = scrapy.Field(output_processor=TakeFirst())
    site = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
    currency = scrapy.Field()

