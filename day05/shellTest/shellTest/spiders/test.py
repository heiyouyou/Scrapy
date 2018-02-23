# -*- coding: utf-8 -*-
import scrapy

class TestSpider(scrapy.Spider):
    name = 'testspider'
    start_urls = [
        'http://example.com/',
        'http://example.net',
        'http://scrapy.org'
    ]

    def parse(self, response):
        if ".org" in response.url:
            from scrapy.shell import inspect_response
            inspect_response(response,self)
        pass