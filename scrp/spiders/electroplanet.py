import datetime

import scrapy


class ElectroplanetSpider(scrapy.Spider):
    name = 'electroplanet'
    allowed_domains = ['electroplanet.ma']

    def start_requests(self):
        yield scrapy.Request(url='https://www.electroplanet.ma', callback=self.parse_urls)

    def parse_urls(self, response):
        for url in response.css('div.sub-sub-item a ::attr(href)').extract():
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        crawled_at = datetime.datetime.utcnow().replace(microsecond=0).isoformat()
        categories = '|'.join(c for c in response.css('div.breadcrumbs ul.items li.item span ::text').extract()[1:])
        for product in response.css('ol.products li.product'):
            yield {
                'title': product.css('img.product-image-photo ::attr(alt)').extract_first(),
                'brand': product.css('span.brand ::text').extract_first(),
                'model': product.css('span.ref ::text').extract_first(),
                'price': int(product.css('.special-price span.price ::text').extract_first().replace(' ', '')) * 100,
                'categories': categories,
                'images': product.css('img.product-image-photo ::attr(src)').extract_first(),
                'link': product.css('a.product-item-link ::attr(href)').extract_first(),
                'available': bool(product.css('span.stock_status_30')),
                'crawled_at': crawled_at
            }
        next_page = response.css('a.next ::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), self.parse)
