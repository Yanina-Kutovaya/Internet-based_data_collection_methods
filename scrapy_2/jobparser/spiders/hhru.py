# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from scrapy_2.jobparser.items import JobparserItem
from scrapy.loader import ItemLoader


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']

    def __init__(self, text):
        self.start_urls = [f'https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&text={text}\
                             &L_save_area=true&area=113&from=cluster_area&showClusters=true']

    def parse(self, response: HtmlResponse):
        vacancy_links = response.xpath("//a[@class='bloko-link HH-LinkModifier']/@href").extract()
        for link in vacancy_links:
            yield response.follow(link, callback=self.vacancy_parse)

        # next_page = response.xpath("//a[@class='bloko-button HH-Pager-Controls-Next HH-Pager-Control']")
        next_page = response.css("a.HH-Pager-Controls-Next::attr(href)").extract_first()
        yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=JobparserItem(), response=response)
        loader.add_css('name', "div.vacancy-title h1::text")
        loader.add_xpath('salary', "//span[@class='bloko-header-2 bloko-header-2_lite']/text()")
        loader.add_value('link', response.url)
        yield loader.load_item()

        #name1 = response.css("div.vacancy-title h1::text").extract_first()
        #salary1 = response.xpath("//span[@class='bloko-header-2 bloko-header-2_lite']/text()").extract()
        #link1 = response.url
        #yield JobparserItem(name=name1, salary=salary1, link=link1)