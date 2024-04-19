from Node import ConfigurationNode
import random
import copy
import time
class Generational:
	def __init__(self):
		self.nodes = []
		self.individuals = 100
		self.generatedIndividuals = []
		self.individual = []
		self.temporalNodes = []
		self.generations = 100
		self.estimate = 0
		self.sum = 0
	def runModel(self):
		for i in range(0,self.individuals):
			print(f"Generando individuo {i+1}")
			self.temporalNodes = copy.deepcopy(self.nodes)
			for node in self.temporalNodes:
				if len(node.ins) == 0:
					self.recursiveGenerateIndividual(node.outs)
			self.generatedIndividuals.append(self.temporalNodes)
			self.temporalNodes = []
		self.evaluateFitness()
	def checkError(self):
		for i in range(0,self.individuals):
			for node in self.nodes:
				if len(node.ins) == 0:
					self.printMemoryAddress(node.outs)
	def printMemoryAddress(self, outs):
		if len(outs) != 0:
			for out in outs:
				print(out)
				self.printMemoryAddress(out.node.outs)
		else:
			print("termina")
	def evaluateFitness(self):
		count = 0
		for individual in self.generatedIndividuals:
			print("\033[H\033[J", end="")
			print('\x1B[1;0H')
			print(f"Evaluando individuo {count+1}")
			count = count + 1
			for node in individual:
				if len(node.outs) == 0:
					self.estimate += node.cars
			for node in individual:
				if len(node.ins) == 0:
					self.recursiveEvaluateFitness(node)
			print(f"Estimado {self.estimate} y obtenido {self.sum}")
			time.sleep(0.25)
			self.estimate = 0
			self.sum = 0
	def recursiveEvaluateFitness(self,node):
		if len(node.outs) != 0:
			for out in node.outs:
				temporal = int(node.cars * out.generated / 100)
				#print(out.generated, temporal)
				if temporal > int(out.max_cars): temporal = int(out.max_cars)
				out.node.cars = temporal
				self.recursiveEvaluateFitness(out.node)
		else:
			self.sum += node.cars
	def recursiveGenerateIndividual(self, outs):
		percentage = 100
		if len(outs) != 0:
			for out in outs:
				#print(out)
				#print(f"Generated before: {out.generated}")
				percentage = 2 if percentage <= 1 else percentage
				generated = random.randint(1,percentage);
				if generated < int(out.max_percentage): out.generated = int(out.max_percentage)
				else: out.generated = generated
				percentage = percentage - generated
				#print(f"Genera {out.generated} y se va al nodo {out.node.index}")
				self.recursiveGenerateIndividual(out.node.outs)
