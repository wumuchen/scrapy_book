# -*- coding: utf-8 -*-
import scrapy
import re


class JdSpider(scrapy.Spider):
	name = 'jd'
	allowed_domains = ['jd.com', '360buyimg.com']
	start_urls = ['http://list.jd.com/list.html?cat=1713,3287,3797']

	def parse(self, response):
		li_list = response.xpath('//div[@id="plist"]/ul/li')
		for li in li_list:
			item = {}
			item["title"] = li.xpath('.//em/text()').extract_first().strip()
			item["href"] = response.urljoin(li.xpath('.//div[@class="p-img"]/a/@href').extract_first())
			item["book_id"] = re.findall(r"(\d+)", item["href"])[0]
			item["img"] = li.xpath('.//div[@class="p-img"]//img/@data-lazy-img').extract_first()
			if item["img"] is None:
				item["img"] = li.xpath('.//div[@class="p-img"]//img/@src').extract_first()
			item["img"] = response.urljoin(item["img"])
			yield scrapy.Request(
				item["img"],
				callback=self.parse_img,
				meta={"item":item},
			)

	def parse_img(self, response):
		item = response.meta["item"]
		with open("images/%s.jpg" % item["book_id"], "wb") as f:
			f.write(response.body)
		print(item)
		# yield item
