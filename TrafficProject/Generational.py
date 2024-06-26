from Individual import Individual
import random
import time


class Generational:
	def __init__(self):
		self.nodes = []
		self.population = 100
		self.for_each_m_generation = 10
		self.do_n_mutation = 5
		self.generation_based_end = False
		self.completion_criteria = 0
		self.stop = True
		self.last_efficiency = 0
		self.individuals = []
	def run_model(self, canvas, font, root, run_data):
		self.stop = False
		for i in range(0, self.population):
			canvas.delete('generated')
			print("\033[H\033[J", end="")
			print('\x1B[1;0H')
			print(f"Generate individual {i+1}")
			run_data.configure(text=f"Generate individual {i+1}")
			self.individuals.append(Individual(self.nodes, canvas, font, root))
		if self.generation_based_end:
			for i in range(self.completion_criteria):
				if not self.stop:
					self.do_generation(canvas, i, run_data)
				else:
					break
		else:
			count = 0
			while True:
				if self.last_efficiency > self.completion_criteria or self.stop:
					break
				self.do_generation(canvas, count,  run_data)
				count += 1
		sorted_individuals = sorted(self.individuals, key=lambda x: x.aptitude, reverse=True)
		# print(sorted_individuals[0].gens[0].outs[0].generated, sorted_individuals[0].gens[0].outs[1].generated)

	def do_generation(self, canvas, i, run_data):
		canvas.delete('generated')
		for individual in self.individuals:
			individual.evaluate_fitness()
		parents = self.roulette_selection()
		sorted_individuals = sorted(self.individuals, key=lambda x: x.aptitude, reverse=True)
		print(f'Best individual of {i + 1} generation is {sorted_individuals[0].aptitude}')
		for index in range(0, len(parents), 2):
			child_a, child_b = self.crossover(parents[index], parents[index + 1])
			self.individuals[index].gens = child_a
			self.individuals[index + 1].gens = child_b
		if i % self.for_each_m_generation == 0:
			print("doing mutations")
			self.do_mutations()
		run_data.configure(text=f'\uf0c0 {i + 1} \uf2f5\uf5e4 {sorted_individuals[0].aptitude} % {sorted_individuals[0].aptitude / sorted_individuals[0].estimate * 100}')
		self.last_efficiency = sorted_individuals[0].aptitude/sorted_individuals[0].estimate * 100
		sorted_individuals[0].draw_individual()

	def do_mutations(self):
		count_mutations = 0
		while count_mutations < self.do_n_mutation:
			individual = random.choice(self.individuals)
			gen = random.choice(individual.gens)
			count_mutations += 1
			percentage = 100
			for out in gen.outs:
				if out == gen.outs[-1]:
					out.generated = percentage
				else:
					if percentage > 1:
						out.generated = random.randint(1, percentage)
					else:
						out.generated = 0
				percentage -= out.generated
	def roulette_selection(self):
		random.shuffle(self.individuals)
		total = sum(individual.aptitude for individual in self.individuals)
		parents = []
		for _ in range(len(self.individuals)):
			spin = random.uniform(0, total)
			carry = 0
			for individual in self.individuals:
				carry += individual.aptitude
				if carry >= spin:
					parents.append(individual)
					break
		return parents
	def crossover(self, parent_a, parent_b):
		limit = random.randint(1, len(self.individuals) - 1)
		child_a = parent_a.gens[:limit] + parent_b.gens[limit:]
		child_b = parent_b.gens[:limit] + parent_a.gens[limit:]
		return child_a, child_b
