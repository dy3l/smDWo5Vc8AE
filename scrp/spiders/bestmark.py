import datetime

import scrapy


class BestmarkSpider(scrapy.Spider):
    name = 'bestmark'
    allowed_domains = ['bestmark.ma']

    def start_requests(self):
        yield scrapy.Request(url='https://www.bestmark.ma', callback=self.parse_urls)

    def parse_urls(self, response):
        for url in response.css('div.sm_megamenu_title div.sm_megamenu_title div.sm_megamenu_title a ::attr(href)').extract():
            yield scrapy.Request(f'{url}?product_list_limit=30', callback=self.parse)

    def parse(self, response):
        crawled_at = datetime.datetime.utcnow().replace(microsecond=0).isoformat()
        categories = '|'.join([c.strip() for c in response.css('ul li.item ::text').extract() if c.strip()][2:])
        for product in response.css('ol.products li.product'):
            yield {
                'title': product.css('img.product-image-photo ::attr(alt)').extract_first(),
                'brand': None,
                'model': None,
                'price': int(''.join(product.css('span.price ::text').extract_first().split()[:-1]).split(',')[0]) * 100,
                'categories': categories,
                'images': product.css('img.product-image-photo ::attr(src)').extract_first(),
                'link': product.css('a.product-item-link ::attr(href)').extract_first(),
                'available': True,
                'crawled_at': crawled_at
            }
        next_page = response.css('a.next ::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), self.parse)
