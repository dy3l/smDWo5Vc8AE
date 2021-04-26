import scrapy


class ElectroplanetSpider(scrapy.Spider):
    name = 'electroplanet'
    allowed_domains = ['electroplanet.ma']
    start_urls = ['http://electroplanet.ma/']

    def parse(self, response):
        pass
