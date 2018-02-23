# -*- coding: utf-8 -*-
import scrapy


class NikeSpider(scrapy.Spider):
    name = 'nike'
    allowed_domains = ['nike.com']
    start_urls = ['http://nike.com/']

    def parse(self, response):
        pass
