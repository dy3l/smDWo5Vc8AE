import datetime

import scrapy


class CosmoselectroSpider(scrapy.Spider):
    name = 'cosmoselectro'
    allowed_domains = ['cosmoselectro.ma']

    def start_requests(self):
        yield scrapy.Request(url='https://www.cosmoselectro.ma', callback=self.parse_urls)

    def parse_urls(self, response):
        for url in response.css('ul.sub-menu li.level2 a ::attr(href)').extract():
            yield scrapy.Request(f'{url}?product_list_limit=40', callback=self.parse)

    def parse(self, response):
        crawled_at = datetime.datetime.utcnow().replace(microsecond=0).isoformat()
        categories = '|'.join(c.strip() for c in response.css('div.breadcrumbs ul.items li.item ::text').extract() if c.strip())
        for product in response.css('ol.products li.product'):
            yield {
                'title': product.css('a.product-item-link ::text').extract_first().strip(),
                'brand': None,
                'model': None,
                'price': int(product.css('span.price-wrapper ::attr(data-price-amount)').extract_first()) * 100,
                'categories': categories,
                'images': product.css('img.product-image-photo ::attr(data-src)').extract_first(),
                'link': product.css('a.product-item-link ::attr(href)').extract_first().strip(),
                'available': True,
                'crawled_at': crawled_at
            }
        next_page = response.css('a.next ::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), self.parse)
