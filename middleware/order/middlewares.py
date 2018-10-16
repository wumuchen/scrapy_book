# 满100减10元!
class Full100Sub10:
	def process_order(self, discount, user, order, order_goods_list):
		if order["total"] > 100:
			order["payTotal"] -= 10
		return order

# 两件8折!
class Count2Off80:
	def process_order(self, discount, user, order, order_goods_list):
		order["total"] = 0
		order["payTotal"] = 0
		for g in order_goods_list:
			if g["count"] >= 2:
				g["total"] = g["price"] * g["count"]
				g["payTotal"] = g["price"] * g["count"] * 0.8
			order["total"] += g["total"]
			order["payTotal"] += g["payTotal"]
		return order
