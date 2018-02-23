# -*- coding:utf-8 -*-
import scrapy

class QuotesSpider(scrapy.Spider):
	name = "quotes"

	# def start_requests(self):
	# 	urls = [
	# 		'http://quotes.toscrape.com/page/1/',
 #            'http://quotes.toscrape.com/page/2/',
	# 	]
	# 	for url in urls:
	# 		yield scrapy.Request(url=url,callback=self.parse)
	# 以上注释代码等同于：
	start_urls = [
		'http://quotes.toscrape.com/page/1/',
	]

	def parse(self,response):
		# page = response.url.split("/")[-2]
		# # print '---------'
		# # print response.url
		# filename = 'quotes-%s.html' % page
		# with open(filename,'wb') as f:
		# 	# 将每个请求的页面数据写入文件中
		# 	f.write(response.body)
		# self.log('Saved file %s' % filename)

		for quote in response.css("div.quote"):
			yield {
				'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
			}
		# next_page = response.css('li.next a::attr(href)').extract_first()
		# if next_page is not None:
		# 	next_page = response.urljoin(next_page)
		# 	# 跟踪下一页的链接数据
		# 	# yield scrapy.Request(next_page,callback=self.parse)

		# 	# 可以替代上面的请求发出，并且response.follow()支持相对路径的值
		# 	yield response.follow(next_page,callback=self.parse)

		for a in response.css('li.next a'):
			yield response.follow(a,callback=self.parse)

