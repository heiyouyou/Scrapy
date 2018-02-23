# -*- coding: utf-8 -*-
import scrapy


class MydomainSpider(scrapy.Spider):
    name = 'mydomain'
    allowed_domains = ['https://doc.scrapy.org']
    start_urls = ['https://doc.scrapy.org/']

    def parse(self, response):
        pass
