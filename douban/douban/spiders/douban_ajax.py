# -*- coding:utf-8 -*-

import re
import json

from scrapy.http import Request
from scrapy.spiders import Spider
from douban.items import DoubanItem

class DoubanAjaxSpider(Spider):
    name = 'douban_ajax'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        url = 'https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start=0&limit=20'
        yield Request(url)

    def parse(self, response):
        datas = json.loads(response.body)
        item = DoubanItem()
        if datas:
            for data in datas:
                # item['movie_name'] = data['title']
                # item['ranking'] = data['rank']
                # item['score'] = data['score']
                # item['score_num'] = data['vote_count']
                # item['movie_pic'] = data['cover_url']
                item.update(movie_name=data['title'],ranking=data['rank'],score=data['score'],score_num=data['vote_count'],movie_pic=data['cover_url'])
                yield item

            # datas存在数据，则进行下一页数据的采集
            page_start = re.search(r'start=(\d+)',response.url).group(1)
            page_start = 'start='+str(int(page_start)+20)
            # next_url = re.sub(r'start=\d+',page_start,response.url)
            # or
            next_url = re.compile(r'start=\d+').sub(page_start,response.url)
            yield Request(next_url)