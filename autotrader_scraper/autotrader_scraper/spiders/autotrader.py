import scrapy


class AutotraderSpider(scrapy.Spider):
    name = 'autotrader'
    allowed_domains = ['autotrader.com']
    start_urls = ['http://autotrader.com/']

    def parse(self, response):
        pass
