import scrapy

class DmozSpider(scrapy.Spider):
	name = "dmoz"
	allowed_domains = ["dmoz.org"]
	start_urls = [
		"http://woodenrobot.me/",
	]
	def parse(self,response):
		filename = response.url.split("/")[-2]
		print filename
		with open(filename,"wb") as f:
			f.write(response.body)