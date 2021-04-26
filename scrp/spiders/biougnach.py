import scrapy


class BiougnachSpider(scrapy.Spider):
    name = 'biougnach'
    allowed_domains = ['biougnach.ma']
    start_urls = ['http://biougnach.ma/']

    def parse(self, response):
        pass
