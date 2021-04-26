import scrapy


class CosmoselectroSpider(scrapy.Spider):
    name = 'cosmoselectro'
    allowed_domains = ['cosmoselectro.ma']
    start_urls = ['http://cosmoselectro.ma/']

    def parse(self, response):
        pass
