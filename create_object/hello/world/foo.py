class Foo:
	def __init__(self, name, age=1):
		self.name = name
		self.age = age

	def hello(self):
		print("hello %s, age %d" % (self.name, self.age))
