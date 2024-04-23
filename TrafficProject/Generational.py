from Node import ConfigurationNode
from Individual import Individual
import random
import copy
import time
class Generational:
	def __init__(self):
		self.nodes = []
		self.population = 100
		self.individuals = []
		self.generations = 500
	def runModel(self, canvas, font, root):
		for i in range(0,self.population):
			canvas.delete('generated')
			print("\033[H\033[J", end="")
			print('\x1B[1;0H')
			print(f"Generate individual {i+1}")
			self.individuals.append(Individual(self.nodes, canvas, font, root))
			time.sleep(0.025)
		for i in range(self.generations):
			print("\033[H\033[J", end="")
			print('\x1B[1;0H')
			canvas.delete('generated')
			parentA, parentB = self.ruletteSelection()
			childA, childB = self.crossover(parentA, parentB)
			sortedIndividuals = sorted(self.individuals, key=lambda x: x.aptitude, reverse=True)
			self.individuals[-2].gens = childA
			self.individuals[-2].evaluate_fitness()
			self.individuals[-1].gens = childB
			self.individuals[-1].evaluate_fitness()
			print(f'Best individual of {i+1} generation is {sortedIndividuals[0].aptitude}')
			sortedIndividuals[0].draw_individual()
			time.sleep(0.025)
		sortedIndividuals = sorted(self.individuals, key=lambda x: x.aptitude, reverse=True)
		print(sortedIndividuals[0].gens[0].outs[0].generated,sortedIndividuals[0].gens[0].outs[1].generated)
	def ruletteSelection(self):
		random.shuffle(self.individuals)
		total = sum(individual.aptitude for individual in self.individuals)
		parents = []
		for _ in range(2):
			spin = random.uniform(0, total)
			carry = 0
			for individual in self.individuals:
				carry += individual.aptitude
				if carry >= spin:
					parents.append(individual)
					break
		return parents
		if len(outs) != 0:
			for out in outs:
				print(out)
				self.printMemoryAddress(out.node.outs)
		else:
			print("termina")
	def crossover(self, parentA, parentB):
		limit = random.randint(1, len(self.individuals) - 1)
		childA = parentA.gens[:limit] + parentB.gens[limit:]
		childB = parentB.gens[:limit] + parentA.gens[limit:]
		return childA, childB