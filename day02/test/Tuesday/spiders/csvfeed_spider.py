from scrapy.spiders import CSVFeedSpider
from Tuesday.items import TuesdayItem

class MySpider(CSVFeedSpider):
	name = 'example.com'
	allowed_domains = ['example.com']
    start_urls = ['http://www.example.com/feed.csv']
    delimiter = ';'
    quotechar = "'"
    headers = ['id','name','description']

    def parse_row(self,response,row):
    	self.logger.info('Hi,this is a row!: %r',row)
    	item = TuesdayItem()
    	item['id'] = row['id']
    	item['name'] = row['name']
    	item['description'] = row['description']
    	return item