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
			time.sleep(0.025)
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
		print(sorted_individuals[0].gens[0].outs[0].generated, sorted_individuals[0].gens[0].outs[1].generated)

	def do_generation(self, canvas, i, run_data):
		print("\033[H\033[J", end="")
		print('\x1B[1;0H')
		canvas.delete('generated')
		parents = self.roulette_selection()
		for index in range(0, len(parents), 2):
			child_a, child_b = self.crossover(parents[index], parents[index + 1])
			self.individuals[index].gens = child_a
			self.individuals[index].evaluate_fitness()
			self.individuals[index + 1].gens = child_b
			self.individuals[index + 1].evaluate_fitness()
		if i % self.for_each_m_generation == 0:
			print("doing mutations")
		sorted_individuals = sorted(self.individuals, key=lambda x: x.aptitude, reverse=True)
		print(f'Best individual of {i + 1} generation is {sorted_individuals[0].aptitude}')
		run_data.configure(text=f'\uf0c0 {i + 1} \uf2f5\uf5e4 {sorted_individuals[0].aptitude} % {sorted_individuals[0].aptitude / sorted_individuals[0].estimate * 100}')
		self.last_efficiency = sorted_individuals[0].aptitude/sorted_individuals[0].estimate * 100
		sorted_individuals[0].draw_individual()
		time.sleep(0.025)

	def do_mutations(self):
		count_mutations = 0
		while count_mutations < self.do_n_mutation:
			individual = random.choice(self.individuals)
			gen = random.choice(individual.gens)
			if len(gen.outs) <= 1:
				continue
			else:
				percentage = 100 - sum(int(out.max_percentage) for out in gen.outs)
				for out in gen.outs:
					percentage += int(out.max_percentage)
					random_percentage = random.randint(1, percentage)
					out.max_percentage = random_percentage
					percentage -= random_percentage
				individual.evaluate_fitness()
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
