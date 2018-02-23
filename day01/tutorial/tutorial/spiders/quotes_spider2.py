import scrapy


class QuotesSpider2(scrapy.Spider):
    name = "quotes2"

    # 参数提供方法一
    def __init__(self,tag=None,*args,**kwargs):
        super(QuotesSpider2,self).__init__(*args,**kwargs)
        self.start_urls = ['http://quotes.toscrape.com/%s' % tag]

    # 参数提供方法二
    def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
            }

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)