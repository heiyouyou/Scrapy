from scrapy.spiders import SitemapSpider

class Mysider(SitemapSpider):
	sitemap_urls = ['http://www.example.com/robots.txt']
	sitemap_rules = [
		('/shop/','parse_shop')
	]

	other_urls = ['http://www.example.com/about']

	def start_request(self):
		requests = list(super(Mysider,self).start_request())
		requests += [scrapy.Request(x,self.parse_other) for x in self.other_urls]
		return requests

	def parse_shop(self,response):
		pass

	def parse_other(self,response):
		pass