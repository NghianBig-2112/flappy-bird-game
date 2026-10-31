import random

from config import *
from brain import NeuralBrain
from entities import *

# --- Built Geenetic algorithm
class GeneticAlgorithm:
	def selection(self, population):
		# Get top 50% individual bird have best fitness
		sorted_pop = sorted(population, key=lambda b: b.fitness, reverse=True)
		survivors_bird = sorted_pop[:len(sorted_pop) // 2]
		return survivors_bird

	def crossover(self, parent_dad, parent_mom):
		# Crossover: get random each gene from dad and mama
		child_chromosome = []
		for i in range(len(parent_dad.chromosome)):
			d = abs(parent_dad.chromosome[i] - parent_mom.chromosome[i])
			min_val = min(parent_dad.chromosome[i], parent_mom.chromosome[i] - 0.2 * d)
			max_val = max(parent_dad.chromosome[i], parent_mom.chromosome[i] + 0.2 * d)
			child_chromosome.append(random.uniform(min_val, max_val))
		return child_chromosome

	def mutate(self, child_chromosome, mutation_rate=0.1):
		# Mutation gene: ech gene have 10% opportunity for small change
		for i in range(len(child_chromosome)):
			if random.uniform(0, 1) < mutation_rate:
				child_chromosome[i] += random.gauss(mu=MUTATION_RATE, sigma=MUTATION_SIGMA)
		return child_chromosome

	def nex_generation(self, population):
		# Create new generation from present population
		survivors = self.selection(population)
		new_population = []

		# Keep the best individual bird (elitism)
		best_brain = survivors[0].brain
		elite_brain = NeuralBrain(bird_y)
		elite.chromosome = best.chromosome[:]
		print("-" * 30)
		print(elite.chromosome)
		new_population.append(elite)

		# Create the remaining offstring using crossover + mutate
		while len(new_population) < POP_SIZE:
			parent_dad = random.choice(survivors)
			parent_mom = random.choice(survivors)
			child = Bird(bird_y)
			child.chromosome = self.crossover(parent_dad, parent_mom)
			child.chromosome = self.mutate(child.chromosome)
			new_population.append(child)
		
		return new_population

def save_best_bird(chromosome, filename="best_bird.json"):
	# save best gene to txt
	with open(filename, "w") as f:
		json.dump(chromosome, f, indent=4)
	print(f"Save model successfully to {filename}")

def load_best_bird(filename="best_bird.json"):
	# Read chromosome from best_bird.txt
	with open(filename, "r") as f:
		chromosome = json.load(f)
	return chromosome