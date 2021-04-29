import scrapy


class BestmarkSpider(scrapy.Spider):
    name = 'bestmark'
    allowed_domains = ['bestmark.ma']
    start_urls = ['http://bestmark.ma/']

    def parse(self, response):
        pass
