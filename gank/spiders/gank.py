# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import FormRequest, Request
from ..items import GankItem
from datetime import timedelta, date
from dateutil.rrule import rrule, DAILY
from ..settings import PULL_RANGE

class HlImageSpider(scrapy.Spider):
	name = 'gank'
	domain = ['gank.io']
	start_urls = (
		'http://gank.io',
	)
	xpath = '//div[@class="typo"]//div[@class="outlink"]//p//img'
	pull_range = PULL_RANGE

	def parse(self,response):
		current_time = str(date.today())
		start_time = str(date.today() - timedelta(days=self.pull_range))

		current_year = current_time.split("-")[0]
		current_month = current_time.split("-")[1]
		current_day = current_time.split("-")[2]

		start_year = start_time.split("-")[0]
		start_month = start_time.split("-")[1]
		start_day = start_time.split("-")[2]

		start_date = date(int(start_year),int(start_month),int(start_day))
		current_date = date(int(current_year),int(current_month),int(current_day))

		for each_date in rrule(DAILY, dtstart=start_date, until=current_date):
			each_year = str(each_date).split("-")[0]
			each_month = str(each_date).split("-")[1]
			each_day = str(each_date).split("-")[2]

			url = self.start_urls[0] + "/" + str(each_year) + "/" + str(each_month) + "/" + str(each_day)
			yield Request(url.split(" ")[0], meta = {'time' : str(each_date)}, callback = self.parse_beauty)

	def parse_beauty(self,response):
		for img_item in response.xpath(self.xpath):
			item = GankItem()
			item['beauty_url'] = img_item.xpath('@src').extract()[0].encode('utf-8').strip()
			item['time'] = response.meta['time']
			yield item