# https://yiyibooks.cn/xx/python_352/library/functions.html
def create_object(class_name, *args, **kwargs):
	cs = class_name.split(".")
	module_name = ".".join(cs[0:-1])
	m = __import__(module_name)
	print(m)
	for i in range(1, len(cs)):
		m = getattr(m, cs[i])
		print(m)
	return m(*args, **kwargs)

if __name__ == '__main__':
	foo = create_object("hello.world.foo.Foo", "张三", age=10)
	foo.hello()
