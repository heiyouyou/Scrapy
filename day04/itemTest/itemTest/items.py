# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,MapCompose,Join
from w3lib.html import remove_tags


class ItemtestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Product(scrapy.Item):
	name = scrapy.Field()
	price = scrapy.Field()
	stock = scrapy.Field()
	last_update = scrapy.Field(serializer=str)


# 扩展Item
class DiscountedProduct(Product):
	discount_percent = scrapy.Field(serializer=str)
	discount_expiration_date = scrapy.Field()


# 声明一个ItemLoader
class ProdutLoader(ItemLoader):
	default_out_processor = TakeFirst()
	name_in = MapCompose(unicode.title)
	name_out = Join()

	price_in = MapCompose(unicode.strip)


def filter_price(value):
	if value.isdigit():
		return value

class Product(scrapy.Item):
	name = scrapy.Field(
		input_processor = MapCompose(remove_tags),
		output_processor = Join()

	)
	price = scrapy.Field(
		input_processor = MapCompose(remove_tags,filter_price),
		output_processor = TakeFirst()
	)




