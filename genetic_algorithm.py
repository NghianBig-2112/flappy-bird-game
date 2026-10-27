import pygame
import math
import numpy as np
import random
import json

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


# --- Color ---
TUBE_COLOR  = (56, 240, 43)
TEXT_COLOR  = (235, 240, 255)

NEON_PINK   = (255, 60, 170)    # chữ Game over
NEON_CYAN   = (60, 230, 255)    # chữ hướng dẫn

# --- Screen ---
WIDTH, HEIGHT = 432, 768

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
running = True
clock = pygame.time.Clock()

# --- Bird ---
BIRD_WIDTH, BIRD_HEIGHT = 51, 36
BIRD_X = WIDTH // 5
bird_y = HEIGHT // 2
GRAVITY = 0.5
bird_velocity = 0	# speed down of bird
FLAP_VELOCITY = 7 	# speed up of bird

# --- Tube ---
TUBE_WIDTH, TUBE_HEIGHT = 78, 480
TUBE_VELOCITY = 2   # Speed of tube move to the left
GATE_HEIGHT = 170	# distance of 2 tubes (tube and tube_inv)

TUBE_INTERVAL = 250	# time next tube appear
tube1_x = WIDTH
tube2_x = tube1_x + TUBE_INTERVAL
tube3_x = tube2_x + TUBE_INTERVAL

# --- Background image ---
background_image = pygame.image.load("assets/background-day.png").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
# --- Bird image ---
bird_image = pygame.image.load("assets/yellowbird-midflap.png").convert_alpha()
bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT))

# --- Tube down image ---
tube_image_down = pygame.image.load("assets/pipe-green.png").convert_alpha()
tube_image_down = pygame.transform.scale(tube_image_down, (TUBE_WIDTH, TUBE_HEIGHT))
# --- Tube top image ---
tube_image_top = pygame.transform.flip(tube_image_down, False, True)

# --- Gameover image ---
gameover_image = pygame.image.load("assets/gameover.png").convert_alpha()

class Bird:
	def __init__(self, y):
		self.x = BIRD_X
		self.y = y
		self.velocity = bird_velocity
		self.flap = FLAP_VELOCITY
		self.image = bird_image

		# --- GA attributes ---
		self.chromosome = [random.uniform(-3, 3) for i in range(6)]	# gene bird
		self.fitness = 0
		self.alive = True
		self.time_alive = 0
		self.score = 0

	def fly_up(self):
		self.velocity = 0
		self.velocity -= self.flap

	def fly_down(self):
		self.y += self.velocity
		self.velocity += GRAVITY

	def get_rect(self):
		return pygame.Rect(self.x, self.y, BIRD_WIDTH, BIRD_HEIGHT)

	# decide jump?
	def think(self, inputs):
		'''
		inputs[0] = bird.y              # vị trí chim (đang cao hay thấp?)
		inputs[1] = bird.velocity  		# đang rơi nhanh hay chậm?
		inputs[2] = dist_to_tube        # cách cột bao xa?
		inputs[3] = gap_top_y           # khe hở phía trên ở đâu?
		inputs[4] = gap_bottom_y        # khe hở phía dưới ở đâu?

		neuron: y = w * x + b
		-> y = w1 * x1 + w2 * x2 + w3 * x3 + w4 * x4 + w5 * x5 + b
		'''
		y = 0
		for i in range(len(inputs)):
			y += self.chromosome[i] * inputs[i]
		y += self.chromosome[-1]

		# use sigmoid function to decide (output: 0.0 to 1.0)
		output = 1 / (1 + np.exp(-y))

		if output > 0.45 and self.velocity > 0:
			self.fly_up()

class Tube:
	def __init__(self, x):
		self.x = x
		self.y = random.randint(int(HEIGHT * 0.3), int(HEIGHT * 0.6))
		self.tube_image_down = tube_image_down
		self.tube_image_top = tube_image_top
		self.passed = False

# --- Built Geenetic algorithm
class GeneticAlgorithm:
	def selection(self, population):
		# Choose top 50% individual bird have best fitness
		sorted_pop = sorted(population, key=lambda b: b.fitness, reverse=True)
		survivors_bird = sorted_pop[:len(sorted_pop) // 2]
		return survivors_bird

	def crossover(self, parent_dad, parent_mom):
		# Crossover: get random each gene from dad and mama
		child_chromosome = []
		for i in range(len(parent_dad.chromosome)):
			if random.uniform(0, 1) < 0.5:
				child_chromosome.append(parent_dad.chromosome[i])
			else:
				child_chromosome.append(parent_mom.chromosome[i])
		return child_chromosome

	def mutate(self, child_chromosome, mutation_rate=0.1):
		# Mutation gene: ech gene have 10% opportunity for small change
		for i in range(len(child_chromosome)):
			if random.uniform(0, 1) < mutation_rate:
				child_chromosome[i] += random.gauss(mu=0, sigma=0.3)
		return child_chromosome

	def nex_generation(self, population):
		# Create new generation from present population
		survivors = self.selection(population)
		new_population = []

		# Keep the best individual bird (elitism)
		best = survivors[0]
		elite = Bird(bird_y)
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

# init object
POP_SIZE = 30
N_INPUTS = 5     # number input of no ron
N_WEIGHTS = 6
population_bird = [Bird(bird_y) for _ in range(POP_SIZE)]
saved_gene = load_best_bird("best_bird.json")
if saved_gene:
	population_bird[0].chromosome = saved_gene
	print("Con chim số 0 đang sử dụng bộ gene vô địch đã lưu!")
tubes = [
	Tube(tube1_x),
	Tube(tube2_x),
	Tube(tube3_x)
]

# --- Init Genetic Algorithm
ga_model = GeneticAlgorithm()
generation = 1

# --- Variable caculate ---
score = 0
font = pygame.font.SysFont("sans", 20)
# is program continue?
pausing = False

# Get x information
def get_inputs(bird, tube):
	# index of bird
	bird_y_center = bird.y + BIRD_HEIGHT // 2
	# bird velocity
	bird_velo = bird.velocity
	# distance bird to nearest tube
	dis_nearest_tube = tube.x - (bird.x + BIRD_WIDTH // 2)
	# distance to top and bottum tube
	dis_top_tube = bird_y_center - tube.y
	dis_buttom_tube = (tube.y + GATE_HEIGHT) - bird_y_center

	return [
		bird_y_center / HEIGHT,
		bird_velo / 10,
		dis_nearest_tube / WIDTH,
		dis_top_tube / HEIGHT,
		dis_buttom_tube / HEIGHT
	]


while running:
	clock.tick(60)  # fps 
			
	# Draw background
	screen.blit(background_image, (0, 0))

	# --- Find nearest tube ---
	nearest_tube = None
	for tube in tubes:
		# check tube in ahead bird and in vision of bird
		if tube.x + TUBE_WIDTH >= BIRD_X:
			if nearest_tube is None or tube.x < nearest_tube.x:
				nearest_tube = tube
		

	# --- Update live bird ---
	alive_birds = [b for b in population_bird if b.alive]

	for bird in alive_birds:
		# increate survival time
		bird.time_alive += 1

		# bird thingking and decide flap?
		if nearest_tube:
			# Draw 2 line from bird center to top_tube and bottom_tube
			pygame.draw.line(screen, NEON_PINK, (bird.x + BIRD_WIDTH //2, bird.y + BIRD_HEIGHT // 2), (nearest_tube.x, nearest_tube.y), width=2)
			pygame.draw.line(screen, NEON_CYAN, (bird.x + BIRD_WIDTH //2, bird.y + BIRD_HEIGHT // 2), (nearest_tube.x, nearest_tube.y + GATE_HEIGHT), width=2)
			inputs = get_inputs(bird, nearest_tube)
			bird.think(inputs)
			
		# Check collide with sky and base
		if bird.y <= 0 or bird.y + BIRD_HEIGHT >= HEIGHT:
			bird.alive = False
			# pausing = True

		# bird down
		if not pausing:
			bird.fly_down()

	# Draw tube
	for tube in tubes:
		# Draw tube inverse
		tube_rect_top = screen.blit(tube_image_top, (tube.x, tube.y - TUBE_HEIGHT))
		# Draw tube 
		tube_rect_down = screen.blit(tube_image_down, (tube.x, tube.y + GATE_HEIGHT))

		# Move tube to the left
		if not pausing:
			tube.x -= TUBE_VELOCITY

		# Check collision with survival bird
		for bird in alive_birds:
			bird_rect = bird.get_rect()
			for obj in [tube_rect_top, tube_rect_down]:
				if bird_rect.colliderect(obj):
					bird.alive = False
					# pausing = True


		# Update score and check first pass for each bird
		for bird in alive_birds:
			if tube.x + TUBE_WIDTH <= BIRD_X and not tube.passed:
				bird.score += 1
				# terminal
				if bird.score == 50:
					pausing = True
					save_best_bird(bird.chromosome, "best_bird.json")
		if tube.x + TUBE_WIDTH <= BIRD_X and not tube.passed:
			# check tube pass all live bird
			tube.passed = True

		# Generate new tubes
		if tube.x <= -TUBE_WIDTH:
			tube.x += len(tubes) * TUBE_INTERVAL
			tube.y = random.randint(int(HEIGHT * 0.3), int(HEIGHT * 0.6))
			tube.passed = False		# Not plus score

	# --- Draw all survival bird ---
	for bird in alive_birds:
		screen.blit(bird.image, (bird.x, bird.y))


	if pausing:
		screen.blit(gameover_image, (100, 100))
		game_over_txt = font.render("Game over, score:" + str(score), True, TEXT_COLOR)
		screen.blit(game_over_txt, (WIDTH // 2 - 110, 200))
		press_space_txt = font.render("Press space to continue", True, TEXT_COLOR)
		screen.blit(press_space_txt, (WIDTH // 2 - 110, 240))

	# --- Hiển thị thông tin ---
	gen_txt   = font.render(f"Generation: {generation}", True, TEXT_COLOR)
	alive_txt = font.render(f"Alive: {len(alive_birds)}/{POP_SIZE}", True, TEXT_COLOR)
	best_txt  = font.render(f"Best score: {max(b.score for b in population_bird)}", True, TEXT_COLOR)
	screen.blit(gen_txt,   (10, 10))
	screen.blit(alive_txt, (10, 35))
	screen.blit(best_txt,  (10, 60))

	# --- if all survival bird dead -> create new generation
	if len(alive_birds) == 0:
		# Calculate fitness for each bird
		for bird in population_bird:
			bird.fitness = bird.score * 100 + bird.time_alive

		# create new generation
		population_bird = ga_model.nex_generation(population_bird)
		generation += 1

		# Reset tube
		tubes = [
			Tube(tube1_x),
			Tube(tube2_x),
			Tube(tube3_x)
		]

	# --- Event button
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			# Quit the program
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				if pausing:
					bird.y = bird_y
					bird.velocity = 0
					score = 0
					tubes = [
						Tube(tube1_x),
						Tube(tube2_x),
						Tube(tube3_x)
					]
					pausing = False
				else:
					bird.fly_up()
	pygame.display.flip()
pygame.quit()