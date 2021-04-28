import scrapy


class MarocventeSpider(scrapy.Spider):
    name = 'marocvente'
    allowed_domains = ['marocvente.com']
    start_urls = ['http://marocvente.com/']

    def parse(self, response):
        pass
