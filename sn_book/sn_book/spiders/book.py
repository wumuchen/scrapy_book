# -*- coding: utf-8 -*-
import scrapy
import re
import json


class BookSpider(scrapy.Spider):
	name = 'book'
	allowed_domains = ['suning.com', 'suning.cn']
	start_urls = ['http://book.suning.com/']

	# def parse(self, response):
	# 	# 分组 一级分类
	# 	div_list = response.xpath('//div[@class="left-menu-container"]//div[@class="menu-item"]')
	# 	for div in div_list:
	# 		cate_1_name = div.xpath('.//h3/a/text()').extract_first()
	# 		cate_1_href = div.xpath('.//h3/a/@href').extract_first()
	# 		# print(cate_1_name)
	# 		# 分组 二级分类
	# 		a2_list = div.xpath('.//dl/dd/a')
	# 		for a2 in a2_list:
	# 			cate_2_name = a2.xpath('./text()').extract_first()
	# 			cate_2_href = a2.xpath('./@href').extract_first()
	# 			# print(cate_2_name)
	# 			# 文档 https://docs.microsoft.com/zh-cn/previous-versions/dotnet/netframework-2.0/ms256456(v%3dvs.80)
	# 			a3_list = response.xpath('//div[@class="submenu-left"]//a[@href="%s"]/../following-sibling::ul[1]/li/a' % cate_2_href)
	# 			for a3 in a3_list:
	# 				cate_3_name = a3.xpath('./text()').extract_first()
	# 				cate_3_href = a3.xpath('./@href').extract_first()
	# 				# print(cate_3_name)
	# 				category = {
	# 					"cate_1_name":cate_1_name, "cate_1_href":cate_1_href,
	# 					"cate_2_name":cate_2_name, "cate_2_href":cate_2_href,
	# 					"cate_3_name":cate_3_name, "cate_3_href":cate_3_href,
	# 				}
	# 				# print(category)
	# 				yield scrapy.Request(
	# 					cate_3_href,
	# 					callback = self.parse_list,
	# 					meta={"category":category}
	# 				)

	def parse(self, response):
		# 分组 一级分类
		div_list = response.xpath('//div[@class="left-menu-container"]//div[@class="menu-item"]')
		for i, div in enumerate(div_list):
			cate_1_name = div.xpath('.//h3/a/text()').extract_first()
			cate_1_href = div.xpath('.//h3/a/@href').extract_first()
			# print(cate_1_name)
			# 分组 二级分类
			p_list = response.xpath('//div[@class="left-menu-container"]//div[@class="menu-sub"][%d]/div[@class="submenu-left"]/p' % (i + 1))
			for p in p_list:
				cate_2_name = p.xpath('./a/text()').extract_first()
				cate_2_href = p.xpath('./a/@href').extract_first()
				# print(cate_2_name)
				# 文档 https://docs.microsoft.com/zh-cn/previous-versions/dotnet/netframework-2.0/ms256456(v%3dvs.80)
				a3_list = p.xpath('./following-sibling::ul[1]/li/a')
				for a3 in a3_list:
					cate_3_name = a3.xpath('./text()').extract_first()
					cate_3_href = a3.xpath('./@href').extract_first()
					# print(cate_3_name)
					category = {
						"cate_1_name":cate_1_name, "cate_1_href":cate_1_href,
						"cate_2_name":cate_2_name, "cate_2_href":cate_2_href,
						"cate_3_name":cate_3_name, "cate_3_href":cate_3_href,
					}
					# print("%s-%s-%s" % (category["cate_1_name"],category["cate_2_name"],category["cate_3_name"]))
					# print(category)
					yield scrapy.Request(
						cate_3_href,
						callback = self.parse_list,
						meta={"category":category}
					)
			
	def parse_list(self, response):
		#分组
		li_list = response.xpath('//div[@id="filter-results"]/ul/li')
		for li in li_list:
			item = {}
			item.update(response.meta["category"])
			item["title"] = li.xpath('.//p[@class="sell-point"]/a/text()').extract_first()
			item["href"] = response.urljoin(li.xpath('.//p[@class="sell-point"]/a/@href').extract_first())
			item["img"] = response.urljoin(li.xpath('.//div[@class="img-block"]//img/@src').extract_first())
			# https://ds.suning.cn/ds/generalForTile/000000000104852073__2_0070078847-010-2-0070121210-1--.json
			item["shopid"], item["prodid"] = re.findall(r'https:\/\/product.suning.com\/(\d+)\/(\d+).html', item["href"])[0]
			yield scrapy.Request(
				"https://ds.suning.cn/ds/generalForTile/000000000%s__2_%s-010-2-0070121210-1--.json" % (item["prodid"], item["shopid"]),
				callback=self.parse_price,
				meta={"item":item}
			)
		# 下一页
		# 当前页 https://list.suning.com/1-262669-0.html
		current_cate, current_page = re.findall(r'https://list.suning.com/\d+-(\d+)-(\d+).html', response.url)[0]
		current_page = int(current_page)
		# print(current_cate, current_page)
		# 总数量 <input type="hidden" value="3712" id="totalCount">
		total = int(response.xpath('//input[@id="totalCount"]/@value').extract_first())
		if (current_page + 1) * 60 < total:
			yield scrapy.Request(
				"https://list.suning.com/1-%s-%d.html" % (current_cate, current_page + 1),
				callback=self.parse_list,
				meta={"category": response.meta["category"]}
			)

	def parse_price(self, response):
		item = response.meta["item"]
		data = json.loads(response.body.decode())
		item["price"] = data["rs"][0]["price"]
		yield scrapy.Request(
			item["href"],
			callback=self.parse_detail,
			meta={"item":item}
		)
	
	def parse_detail(self, response):
		item = response.meta["item"]
		item["author"] = response.xpath('.//span[text()="作者："]/../text()').extract_first()
		print(item)

