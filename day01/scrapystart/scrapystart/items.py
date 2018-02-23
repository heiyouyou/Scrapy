# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapystartItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DomzItem(scrapy.Item):
	name = Field()
	description = Field()
	url = Field()
