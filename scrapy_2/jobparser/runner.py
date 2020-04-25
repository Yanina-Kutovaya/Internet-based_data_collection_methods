from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy_2.jobparser import settings
from scrapy_2.jobparser.spiders.hhru import HhruSpider
from scrapy_2.jobparser.spiders.sj import SjSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhruSpider, text="python")
    process.crawl(SjSpider, text="python")
    process.start()
