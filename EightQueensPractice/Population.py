from Individual import Individual
class Population:
	def __init__(self, n, generations):
		self.n = n
		self.generations = generations
		self.individuals = []
	
	def runGenerations(self):
		for i in range(self.n):
			self.individuals.append(Individual(id=i))
			self.individuals[i].getAptitude()
		for i in range(self.generations):
			print(f"Doing {i+1} generation")
			self.individuals = sorted(self.individuals, key=lambda x: x.aptitude, reverse=True)
			parentA = self.individuals[0].gens
			parentB = self.individuals[1].gens
			childA = parentA[0:4] + parentB[4:8]
			childB = parentB[0:4] + parentA[4:8]
			self.individuals[6].gens = childA
			self.individuals[6].getAptitude()
			self.individuals[7].gens = childB
			self.individuals[7].getAptitude()
		for i in range(self.n):
			self.individuals[i].printBoard()
			print(self.individuals[i].aptitude)

		
