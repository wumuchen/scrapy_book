from create_object import create_object

# 设计模式

# 优惠规则 模拟数据库里边的数据
discount_table = [
	{"id": 1, "name": "满100减10元!", "class_name": "order.middlewares.Full100Sub10"},
	{"id": 2, "name": "两件8折!", "class_name": "order.middlewares.Count2Off80"},
]

# 模型方法
def get_discount(discount_id):
	for d in discount_table:
		if d["id"] == discount_id:
			return d

# ----- 订单处理 -----

# 用户数据
user = {
	"id": 1,
	"username": "zhangsan",
	"money": 110.00,
}
# 订单明细
order_goods_list = [
	{"goods_id":1, "goods_name":"python高级编程", "price":66.00, "count":1, "total": 66.00, "payTotal": 66.00},
	{"goods_id":2, "goods_name":"scrapy高级编程", "price":53.00, "count":2, "total": 106.00, "payTotal": 106.00},
]
# 订单信息
order = {
	"user_id": user["id"],
	"total": 172.00,
	"payTotal": 172.00,
	"discount": 2
}
# 优惠信息
discount = get_discount(order["discount"])
print(discount)

# 创建优惠中间件对象
order_middleware = create_object(discount["class_name"])

# 处理订单
order = order_middleware.process_order(discount, user, order, order_goods_list)

# 订单价格
print(order)

# 使用if语句实现
if order["discount"] == 1:
	pass
elif order["discount"] == 2:
	pass
