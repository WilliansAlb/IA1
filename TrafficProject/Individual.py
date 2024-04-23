import copy
import random
import time
class Individual:
	def __init__(self, nodes, canvas, font, root):
		self.aptitude = 0
		self.gens = []
		self.nodes = nodes
		self.estimate = 0
		self.canvas = canvas
		self.font = font
		self.root = root
		self.randomize()
	def randomize(self):
		temporal = copy.deepcopy(self.nodes)
		for node in temporal:
			if len(node.outs) == 0:
				self.estimate += node.cars
		for node in temporal:
			if len(node.ins) == 0:
				self.recursive_generate(node.outs)
		self.gens = temporal
		self.evaluate_fitness()
	def evaluate_fitness(self):
		self.aptitude = 0
		for node in self.gens:
			if len(node.ins) != 0:
				node.cars = 0
		for node in self.gens:
			if len(node.ins) == 0:
				self.recursive_evaluate(node)
		#time.sleep(0.05)
		print(f"Estimado {self.estimate} y obtenido {self.aptitude}")
	def recursive_evaluate(self,node):
		if len(node.outs) != 0:
			for out in node.outs:
				temporal = int(node.cars * out.generated / 100)
				#print(out.generated, temporal)
				if temporal > int(out.max_cars): temporal = int(out.max_cars)
				out.node.cars = temporal
				self.recursive_evaluate(out.node)
		else:
			self.aptitude += node.cars
	def draw_individual(self):
		for node in self.gens:
			for out in node.outs:
				self.canvas.create_text(out.square.x * 50 + 25, out.square.y * 50+25, text=f"%{out.generated}", fill="white", font=("FontAwesome",12,"bold"), tags='generated')
				self.root.update()
	def recursive_generate(self, outs):
		percentage = 100
		if len(outs) != 0:
			if len(outs) == 0:
				outs[0].generated = 100
				self.recursive_generate(out.node.outs)
			else:
				count = 0
				for out in outs:
					count = count + 1
					if (count != len(outs)):
						percentage = 2 if percentage <= 1 else percentage
						generated = random.randint(1,percentage);
						if generated < int(out.max_percentage): out.generated = int(out.max_percentage)
						else: out.generated = generated
						percentage = percentage - generated
						#print(f"Genera {out.generated} y se va al nodo {out.node.index}")
					else: out.generated = percentage
					self.canvas.create_text(out.square.x * 50 + 25, out.square.y * 50+25, text=f"%{out.generated}", fill="white", font=("FontAwesome",12,"bold"), tags='generated')
					self.root.update()
					self.recursive_generate(out.node.outs)