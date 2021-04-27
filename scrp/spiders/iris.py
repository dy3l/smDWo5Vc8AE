import scrapy


class IrisSpider(scrapy.Spider):
    name = 'iris'
    allowed_domains = ['iris.ma']
    start_urls = ['http://iris.ma/']

    def parse(self, response):
        pass
