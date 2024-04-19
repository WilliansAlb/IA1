class Node:
	def __init__(self, cars, ins, outs, index):
		self.cars = cars
		self.ins = ins
		self.outs = outs
		self.index = index
class ConfigurationNode:
	def __init__(self, node, max_cars, max_percentage, generated):
		self.node = node
		self.max_cars = max_cars
		self.max_percentage = max_percentage
		self.generated = generated