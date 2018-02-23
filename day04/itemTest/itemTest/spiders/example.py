# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from itemTest.items import Product


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']

    def parse(self, response):
        l = ItemLoader(item=Product(),response=response)
        l.add_xpath('name','//div[@class="product_name"]')
        l.add_xpath('name','//div[@class="product_title"]')
        l.add_xpath('price','//p[@id="price"]')
        l.add_css('stock','p#stock')
        l.add_value('last_updated','today')
        return l.load_item()