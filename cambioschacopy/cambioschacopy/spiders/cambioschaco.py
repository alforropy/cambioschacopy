# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CambioschacoSpider(CrawlSpider):
    name = 'cambioschaco'
    allowed_domains = ['cambioschaco.com.py']
    start_urls = ['https://cambioschaco.com.py/']

    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def start_requests(self):
        urls = [
            'https://www.cambioschaco.com.py/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for row in response.xpath('//*[@class="table-exchange-content"]//tbody/tr'):
            yield {
                'moneda' : row.xpath('td//text()')[0].extract().strip(),
                'compra': row.xpath('td//text()')[2].extract().strip(),
                'venta' : row.xpath('td//text()')[5].extract().strip(),
            }