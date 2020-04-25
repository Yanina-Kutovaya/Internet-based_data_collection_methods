# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from scrapy_2.jobparser.items import JobparserItem
from scrapy.loader import ItemLoader


class SjSpider(scrapy.Spider):
    name = 'sj'
    allowed_domains = ['superjob.ru']

    def __init__(self, text):
        self.start_urls = [f'https://russia.superjob.ru/vacancy/search/?keywords={text}']

    def parse(self, response: HtmlResponse):
        s = "https://russia.superjob.ru"
        vacancy_links = response.xpath("//div[@class='acdxh GPKTZ _1tH7S']/div/a/@href").extract()
        for link in vacancy_links:
            yield response.follow(s + link, callback=self.vacancy_parse)

        next_page = s + response.xpath("//a[@class='icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe']/@href").extract_first()
        yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=JobparserItem(), response=response)
        loader.add_css('name', "div._3MVeX h1::text")
        loader.add_xpath('salary', "//span[@class='_3mfro _2Wp8I ZON4b PlM3e _2JVkc']/text()")
        loader.add_value('link', response.url)
        yield loader.load_item()


        #name1 = response.css("div._3MVeX h1::text").extract_first()
        #salary1 = response.xpath("//span[@class='_3mfro _2Wp8I ZON4b PlM3e _2JVkc']/text()").extract()
        #link1 = response.url
        #yield JobparserItem(name=name1, salary=salary1, link=link1)