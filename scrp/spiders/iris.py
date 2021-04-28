import datetime

import scrapy


class IrisSpider(scrapy.Spider):
    name = 'iris'
    allowed_domains = ['iris.ma']

    def start_requests(self):
        yield scrapy.Request(url='https://www.iris.ma', callback=self.parse_urls)

    def parse_urls(self, response):
        for url in response.css('ul.submenu-container a.sf-with-ul ::attr(href)').extract():
            yield scrapy.Request(response.urljoin(url), callback=self.parse)

    def parse(self, response):
        crawled_at = datetime.datetime.utcnow().replace(microsecond=0).isoformat()
        categories = '|'.join([c for c in response.css('div.breadcrumb ::text').extract() if len(c) > 2])
        for product in response.css('ul.product_list li.ajax_block_product'):
            yield {
                'title': product.css('a.product-name ::text').extract_first().strip(),
                'brand': None,
                'model': None,
                'price': int(product.css('span.price ::text').extract_first().strip().split(',')[0].replace(' ', '')) * 100,
                'categories': categories,
                'images': product.css('img ::attr(src)').extract_first(),
                'link': product.css('a.product-name ::attr(href)').extract_first().strip(),
                'available': bool(product.css('span.available-now')),
                'crawled_at': crawled_at
            }
        next_page = response.css('li.pagination_next a ::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), self.parse)
