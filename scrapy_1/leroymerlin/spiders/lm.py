# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from scrapy_1.leroymerlin.items import LeroymerlinItem
from scrapy.loader import ItemLoader


class LmSpider(scrapy.Spider):
    name = 'lm'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, text):
        self.start_urls = [f'https://leroymerlin.ru/search/?q={text}']

    def parse(self, response: HtmlResponse):
        item_links = response.xpath("//div[@class='product-name']/a/@href").extract()
        s = 'https://leroymerlin.ru/'
        for link in item_links:
            yield response.follow(s + link, callback=self.item_parse)

        next_page = s + response.xpath("//div[@class='next-paginator-button-wrapper']/a/@href").extract_first()
        yield response.follow(next_page, callback=self.parse)

    def item_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinItem(), response=response)
        loader.add_css('name', "div.product-content h1::text")
        loader.add_xpath('photos', "//img/@data-origin")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('s_keys', "//dt[@class='def-list__term']/text()")
        loader.add_xpath('s_values', "//dd[@class='def-list__definition']/text()")
        yield loader.load_item()
