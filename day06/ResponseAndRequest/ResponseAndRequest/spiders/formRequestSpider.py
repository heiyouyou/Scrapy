# -*- coding:utf-8 -*-
import scrapy

# 使用FormRequest.from_response()来模拟一个用户登录
class LoginSpider(scrapy.Spider):
	name = 'wifi.com'
	start_ulrs = ['http://116.205.4.18:58080/systemv3/login']

	def parse(self,response):
		return scrapy.FormRequest.from_response(response,formdata={'username':'wifi','password':'Wifi,./123'},callback=self.after_login)

	def after_login(self,response):
		if "authentication failed" in response.body:
			self.logger.error('Login failed')
			return 	