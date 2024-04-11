from Individual import Individual
import random
import time
class Population:
	def __init__(self, n, generations):
		self.n = n
		self.generations = generations
		self.individuals = []
	
	def runGenerations(self):
		print("\033[H\033[J", end="")
		print('\x1B[1;0H')
		for i in range(self.n):
			self.individuals.append(Individual(id=i))
			self.individuals[i].calculateAptitude()
		for i in range(self.generations):
			print('\x1B[2;0H')
			print(f'Best individual of {i+1} generation', end='\n')
			parentA, parentB = self.ruletteSelection()
			childA, childB = self.crossover(parentA, parentB)
			self.individuals = sorted(self.individuals, key=lambda x: x.aptitude, reverse=True)
			self.individuals[-2].gens = childA
			self.individuals[-2].calculateAptitude()
			self.individuals[-1].gens = childB
			self.individuals[-1].calculateAptitude()
			self.individuals[0].printBoard()
			time.sleep(0.100)
		#sortedIndividuals = sorted(self.individuals, key=lambda x: x.aptitude, reverse=True)
		#for i in range(2):
  
	def crossover(self, parentA, parentB):
		limit = random.randint(1, 7)
		childA = parentA.gens[:limit] + parentB.gens[limit:]
		childB = parentB.gens[:limit] + parentA.gens[limit:]
		return childA, childB

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
		
