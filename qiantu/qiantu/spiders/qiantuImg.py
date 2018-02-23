# -*- coding: utf-8 -*-

import json

import scrapy
from scrapy.http import Request
from qiantu.items import QiantuItem

# 计数器
jishu = 1

class QiantuimgSpider(scrapy.Spider):
    name = 'qiantuImgSpider'
    allowed_domains = ['58pic.com']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    # ajax初始化请求数据的地址
    def start_requests(self):
        url = 'http://www.58pic.com/index.php?m=ajaxSearch&a=ajaxGetCategory'
        yield Request(url,headers=self.headers)

    # 分析提取各种分类的url
    def parse(self, response):
        # 获取各种类别的url跳转地址
        # urldata = response.xpath('//div[@class="search-classify"]/p[@class="sec-title"]/a/@href').extract()
        # urldata = response.css('div[class="search-classify"] p[class="sec-title"] a::attr(href)').extract()
        print response.body
        data = json.loads(response.body)
        list = data['cateAllMessage']
        for item in list:
            for v in item.values():
                # 排除不是字典的value
                if isinstance(v,dict):
                    for kid in v['kidList']:
                        # 注意一定要配置headers，否则获取不到数据
                        yield Request(kid['url'],callback=self.next1,headers=self.headers)

    # 获取每类中的每一页的数据
    def next1(self,response):
        # 当前页
        cur_url = response.url
        # 获取每一页中缩略图的详情地址
        url_entry = response.xpath('//div[@class="flow-item qt-card"]/div[@class="card-img"]/a[@class="thumb-box"]/@href').extract()
        for u in url_entry:
            yield Request(u, callback=self.getImg, headers=self.headers)
        #  获取下一页
        u_list = response.xpath('//div[@class="qt-pagination"]/a[contains(@rel,"external nofollow")]/@href').extract()
        # u_list = response.css('div[class="qt-pagination"]>a[rel="external nofollow"]::attr(href)').extract()
        # 排除url为空的情况
        next_url = u_list[1] if u_list else ''
        if next_url:
            yield response.follow(next_url,callback=self.next1,headers=self.headers)

    # 获取真实图片
    def getImg(self,response):
        global jishu
        print(u"此时正爬取第" + str(jishu) + u"个图片---" + response.url + "----")
        print response.xpath('//div[@class="detail-img type-tag"]/img[@class="show-area-pic"]/@title').extract()
        item = QiantuItem()
        item['title'] = response.xpath('//div[@class="detail-img type-tag"]/img[@class="show-area-pic"]/@title').extract()[0]
        item['url'] = response.xpath('//div[@class="detail-img type-tag"]/img[@class="show-area-pic"]/@src').extract()[0]
        jishu +=1
        yield item

