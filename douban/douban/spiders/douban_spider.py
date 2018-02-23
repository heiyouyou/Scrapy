# -*- coding:utf-8 -*-

from scrapy import Request
from scrapy.spiders import Spider
from douban.items import DoubanItem

class DoubanMovieTop250Sipder(Spider):
	name = 'douban_movie_top250'
	# start_urls = ['https://movie.douban.com/top250']

	# 此配置项可以在setting文件的 USER_AGENT 配置
	# headers = {
	# 	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
	# }

	def start_requests(self):
		url = 'https://movie.douban.com/top250'
		# yield Request(url,headers=self.headers)
		yield Request(url)

	def parse(self,response):
		# 命令行调试代码
		# from scrapy.shell import inspect_response
		# inspect_response(response,self)

		# 创建每部电影的Item对象
		item = DoubanItem()
		# xpath选择器获取全部电影的Selector List
		movies = response.xpath("//ol[@class='grid_view']/li")
		for movie in movies:
			item['ranking'] = movie.xpath(".//div[@class='pic']/em/text()").extract()[0]
			item['movie_name'] = movie.xpath(".//div[@class='info']/div[@class='hd']/a/span[1]/text()").extract()[0]
			# 可以使用encode("gbk")解决在windows用户下用excel打开csv文件时乱码的问题，也可以在setting.py文件中全局配置FEED_EXPORT_ENCODING = 'gbk'导出文件时的编码
			# item['movie_name'] = movie.xpath(".//div[@class='info']/div[@class='hd']/a/span[1]/text()").extract()[0].encode("gbk")
			item['score'] = movie.xpath(".//div[@class='info']/div[@class='bd']/div[@class='star']/span[@class='rating_num']/text()").extract()[0]
			item['score_num'] = movie.xpath(".//div[@class='info']/div[@class='bd']/div[@class='star']/span/text()").re(ur"(\d+)人评价")[0]
			item['movie_pic'] = movie.xpath(".//div[@class='pic']/a/img/@src").extract()[0]
			yield item
		# 不能在这里使用索引获取，因为等到获取最后一页的时候会报错
		# next_url = response.xpath("//span[@class='next']/a/@href").extract()[0]
		next_url = response.xpath("//span[@class='next']/a/@href").extract()
		# 继续追踪（请求）下一页的数据
		if next_url:
			next_url = 'https://movie.douban.com/top250'+next_url[0]
			# yield Request(next_url,headers=self.headers)
			yield Request(next_url)

