import pygame
import random
from random import randint
import math

# --- Color ---
TUBE_COLOR  = (56, 240, 43)
TEXT_COLOR  = (235, 240, 255)

# --- Screen ---
WIDTH, HEIGHT = 500, 700

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
running = True
clock = pygame.time.Clock()

# --- Bird ---
BIRD_WIDTH, BIRD_HEIGHT = 40, 28
BIRD_X = WIDTH // 5
bird_y = HEIGHT // 2
GRAVITY = 0.5
bird_velocity = 0	# speed down of bird
JUMP_VELOCITY = 7 	# speed up of bird

# --- Parameter of Genetic Algorithm ----
POP_SIZE = 30   # number of birds per generation
N_INPUTS = 5     # number input of no ron
N_WEIGHTS = 6

# --- Tube ---
TUBE_WIDTH = 50
TUBE_VELOCITY = 2   # Speed of tube move to the left
gate_height = 150	# distance of 2 tubes (tube and tube_inv)

pipe_interval = 250	# time next tube appear
tube1_x = 400
tube2_x = tube1_x + pipe_interval
tube3_x = tube2_x + pipe_interval


# --- Background images ---
background_image = pygame.image.load("assets/background-day.png").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

bird_image = pygame.image.load("assets/yellowbird-midflap.png").convert_alpha()
bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT))

class Bird:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.width = BIRD_WIDTH
		self.height = BIRD_HEIGHT
		self.velocity = bird_velocity
		self.gravity = GRAVITY
		self.jump_velocity = JUMP_VELOCITY
		self.image = bird_image

		# --- GA attributes ---
		self.chromosome = [random.uniform(-2, 2) for _ in range(N_WEIGHTS)]
		self.fitness = 0
		self.alive = True
		self.time_alive = 0
		self.score = 0

	def fly_up(self):
		self.velocity = 0
		self.velocity -= self.jump_velocity

	def fly_down(self):
		self.y += self.velocity
		self.velocity += self.gravity

	def get_rect(self):
		return pygame.Rect(self.x, self.y, self.width, self.height)

	# decide jump ?
	def think(self, inputs):
		'''
		inputs[0] = bird.y              # vị trí chim (đang cao hay thấp?)
		inputs[1] = bird.velocity  # đang rơi nhanh hay chậm?
		inputs[2] = dist_to_pipe        # cách cột bao xa?
		inputs[3] = gap_top_y           # khe hở phía trên ở đâu?
		inputs[4] = gap_bottom_y        # khe hở phía dưới ở đâu?
		'''
		# use neuron y = w * a + b
		total = 0
		for i in range(len(inputs)):
			total += inputs[i] * self.chromosome[i]
		total += self.chromosome[-1]    # bias

		# Usr sigmoid function (output: 0.0 to 1.0)
		output = 1 / (1 + math.exp(-total))

		# decide
		if output > 0.5:
			self.fly_up()


class Tube:
	def __init__(self, x):
		self.x = x
		self.width = TUBE_WIDTH
		self.height = randint(100, HEIGHT // 2 + 20)
		self.gate_height = gate_height
		self.pipe_interval = pipe_interval
		self.velocity = TUBE_VELOCITY
		self.passed = False

class GeneticAlgorithm:

	def selection(self, population):
		"""Chọn top 50% cá thể có fitness cao nhất"""
		sorted_pop = sorted(population, key=lambda b: b.fitness, reverse=True)
		survivors = sorted_pop[:len(sorted_pop) // 2]
		return survivors

	def crossover(self, parent1, parent2):
		"""Lai ghép: mỗi gene lấy ngẫu nhiên từ cha hoặc mẹ"""
		child_chromosome = []
		for i in range(len(parent1.chromosome)):
			if random.random() < 0.5:
				child_chromosome.append(parent1.chromosome[i])
			else:
				child_chromosome.append(parent2.chromosome[i])
		return child_chromosome

	def mutate(self, chromosome, mutation_rate=0.1):
		"""Đột biến: mỗi gene có 10% cơ hội thay đổi nhỏ"""
		for i in range(len(chromosome)):
			if random.random() < mutation_rate:
				chromosome[i] += random.gauss(0, 0.3)
		return chromosome

	def next_generation(self, population):
		"""Tạo thế hệ mới từ quần thể hiện tại"""
		survivors = self.selection(population)
		new_population = []

		# Giữ lại con giỏi nhất (elitism)
		best = survivors[0]
		elite = Bird(BIRD_X, bird_y)
		elite.chromosome = best.chromosome[:]   # copy chromosome
		new_population.append(elite)

		# Tạo các con còn lại bằng crossover + mutate
		while len(new_population) < POP_SIZE:
			p1 = random.choice(survivors)
			p2 = random.choice(survivors)
			child = Bird(BIRD_X, bird_y)
			child.chromosome = self.crossover(p1, p2)
			child.chromosome = self.mutate(child.chromosome)
			new_population.append(child)

		return new_population


# --- Init GA ---
ga = GeneticAlgorithm()
generation = 1

# Tạo quần thể 30 con chim
population = [Bird(BIRD_X, bird_y) for _ in range(POP_SIZE)]

tubes = [
	Tube(tube1_x),
	Tube(tube2_x),
	Tube(tube3_x)
]

font = pygame.font.SysFont("sans", 20)

# definition function
def get_inputs(bird, nearest_tube):
	return [
		bird.y / HEIGHT,                              # [0..1]
		bird.velocity / 20,                     # [-1..1]
		(nearest_tube.x - bird.x) / WIDTH,           # [0..1]
		nearest_tube.height / HEIGHT,                # [0..1]
		(nearest_tube.height + nearest_tube.gate_height) / HEIGHT  # [0..1]
	]


while running:
	clock.tick(60)

	# --- Events ---
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# --- Draw background ---
	screen.blit(background_image, (0, 0))

	# --- Tìm cột gần nhất phía trước ---
	nearest_tube = None
	for tube in tubes:
		if tube.x + tube.width > BIRD_X:
			if nearest_tube is None or tube.x < nearest_tube.x:
				nearest_tube = tube

	# --- Cập nhật từng con chim còn sống ---
	alive_birds = [b for b in population if b.alive]

	for bird in alive_birds:
		# Tăng thời gian sống
		bird.time_alive += 1

		# Cho chim suy nghĩ và quyết định nhảy
		if nearest_tube:
			inputs = get_inputs(bird, nearest_tube)
			bird.think(inputs)

		# Chim rơi xuống
		bird.fly_down()

		# Kiểm tra chạm trần/sàn
		if bird.y <= 0 or bird.y + bird.height >= HEIGHT:
			bird.alive = False

	# --- Di chuyển & vẽ ống ---
	for tube in tubes:
		tube_rect     = pygame.draw.rect(screen, TUBE_COLOR, (tube.x, 0, tube.width, tube.height))
		tube_rect_inv = pygame.draw.rect(screen, TUBE_COLOR, (tube.x, tube.height + tube.gate_height, tube.width, HEIGHT - tube.height - tube.gate_height))

		tube.x -= tube.velocity

		# Kiểm tra va chạm với từng chim sống
		for bird in alive_birds:
			bird_rect = bird.get_rect()
			if bird_rect.colliderect(tube_rect) or bird_rect.colliderect(tube_rect_inv):
				bird.alive = False

		# Cập nhật score riêng cho từng chim
		for bird in alive_birds:
			if tube.x + tube.width <= bird.x and not tube.passed:
				bird.score += 1
		if tube.x + tube.width <= BIRD_X and not tube.passed:
			tube.passed = True

		# Tái tạo ống khi ra ngoài màn hình
		if tube.x <= -tube.width:
			tube.x += len(tubes) * tube.pipe_interval
			tube.height = randint(100, HEIGHT // 2 + 20)
			tube.passed = False

	# --- Vẽ tất cả chim còn sống ---
	for bird in alive_birds:
		screen.blit(bird.image, (bird.x, bird.y))

	# --- Hiển thị thông tin ---
	gen_txt   = font.render(f"Generation: {generation}", True, TEXT_COLOR)
	alive_txt = font.render(f"Alive: {len(alive_birds)}/{POP_SIZE}", True, TEXT_COLOR)
	best_txt  = font.render(f"Best score: {max(b.score for b in population)}", True, TEXT_COLOR)
	screen.blit(gen_txt,   (10, 10))
	screen.blit(alive_txt, (10, 35))
	screen.blit(best_txt,  (10, 60))

	# --- Khi tất cả chim chết → tạo thế hệ mới ---
	if len(alive_birds) == 0:
		# Tính fitness cho từng con
		for bird in population:
			bird.fitness = bird.score * 100 + bird.time_alive

		# Tạo thế hệ mới
		population = ga.next_generation(population)
		generation += 1

		# Reset ống
		tubes = [
			Tube(tube1_x),
			Tube(tube2_x),
			Tube(tube3_x)
		]

	pygame.display.flip()

pygame.quit()