# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import json
import pymongo
import scrapy
import hashlib
from urllib import quote


class ShelltestPipeline(object):
    def process_item(self, item, spider):
        return item

# 过滤不符合的数据 
class PricePipeline(object):
	vat_factor = 1.15
	def process_item(self,item,spider):
		if item['price']:
			if item['price_excludes_vat']:
				item['price'] = item['price']*self.vat_factor
			return item
		else:
			raise DropItem("Missing price in %s" % item)

# 以json的格式将数据写入文件
class JsonWriterPipeline(object):
	def open_spider(self,spider):
		self.file = open('items.jl','w')

	def close_spider(self,spider):
		self.file.close()

	def process_item(self,item,spider):
		line = json.dumps(dict(item))+"\n"
		self.file.write(line)
		return item	

# 将item序列化存入Moongodb
class MongoPipeline(object):
	collection_name = 'scrapy_items'

	def __init__(self,mongo_uri,mongo_db):
		self.mongo_uri = mongo_uri
		self.mongo_db = mongo_db

	@classmethod
	def from_crawler(cls,crawler):
		return cls(
			mongo_uri = crawler.settings.get('MONGO_URI'),
			mongo_db = crawler.settings.get('MONGO_DATABASE','items')
		)

	def open_spider(self,spider):
		self.client = pymongo.MongoClient(self.mongo_uri)
		self.db = self.client[self.mongo_db]

	def close_spider(self,spider):
		self.client.close()

	def process_item(self,item,spider):
		self.db[self.collection_name].insert_one(dict(item))
		return item

# 如何返回一个Defferred对象
class ScreenshotPipeline(object):
	SPLASH_URL = "http://localhost:8050/render.png?url={}"

	def process_item(self,item,spider):
		encoded_item_url = quote(item["url"])
		screenshot_url = self.SPLASH_URL.format(encoded_item_url)
		request = scrapy.Request(screenshot_url)
		dfd = spider.crawler.engine.download(request,spider)
		dfd.addBoth(self.return_item,item)
		return dfd

	def return_item(self,response,item):
		if response.status !=200:
			return item

		url = item["url"]
		url_hash = hashlib.md5(url.encode("utf8")).hexdigest()
		filename = "{}.png".format(url_hash)
		with open(filename,"wb") as f:
			f.write(response.body)

		item["screenshot_filename"] = filename
		return item

# 去重，多个重复的item会具有同一个id
class DuplicatesPipeline(object):
	def __init__(self):
		self.ids_seen = set()

	def process_item(self,item,spider):
		if item['id'] in self.ids_seen:
			raise DropItem("Duplicate item found: %s" %item)
		else:
			self.ids_seen.add(item['id'])
			return item