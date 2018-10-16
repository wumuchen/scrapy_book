# -*- coding: utf-8 -*-
import scrapy
import re
import hashlib


class JdSpider(scrapy.Spider):
	name = 'jd2'
	allowed_domains = ['jd.com', '360buyimg.com']
	start_urls = ['http://list.jd.com/list.html?cat=1713,3287,3797']

	def parse(self, response):
		li_list = response.xpath('//div[@id="plist"]/ul/li')
		for li in li_list:
			item = {}
			item["title"] = li.xpath('.//em/text()').extract_first().strip()
			item["href"] = response.urljoin(li.xpath('.//div[@class="p-img"]/a/@href').extract_first())
			item["book_id"] = re.findall(r"(\d+)", item["href"])[0]
			item["image_urls"] = li.xpath('.//div[@class="p-img"]//img/@data-lazy-img').extract()
			if len(item["image_urls"]) == 0:
				item["image_urls"] = li.xpath('.//div[@class="p-img"]//img/@src').extract()
			item["image_urls"] = [response.urljoin(url) for url in item["image_urls"]]
			yield item

	# def url_to_sha1(self, url):
	# 	fp = hashlib.sha1()
	# 	fp.update(url.encode())
	# 	return fp.hexdigest()