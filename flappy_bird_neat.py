import pygame
from random import randint

# --- Color ---
TUBE_COLOR  = (56, 240, 43)
TEXT_COLOR  = (235, 240, 255)
NEON_PINK   = (255, 60, 170)    # chữ Game over
NEON_CYAN   = (60, 230, 255)    # chữ hướng dẫn

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

# --- Tube ---
TUBE_WIDTH = 50
TUBE_VELOCITY = 2   # Speed of tube move to the left
gate_height = 200	# distance of 2 tubes (tube and tube_inv)

pipe_interval = 250	# time next tube appear
tube1_x = 400
tube2_x = tube1_x + pipe_interval
tube3_x = tube2_x + pipe_interval


# --- Background images ---
background_image = pygame.image.load("assets/Game_Objects/background-day.png").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

bird_image = pygame.image.load("assets/Game_Objects/yellowbird-midflap.png").convert_alpha()
bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT))

class Bird:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.width = BIRD_WIDTH
		self.height = BIRD_HEIGHT
		self.down_velocity = bird_velocity
		self.gravity = GRAVITY
		self.jump_velocity = JUMP_VELOCITY
		self.image = bird_image

	def fly_up(self):
		self.down_velocity = 0
		self.down_velocity -= self.jump_velocity

	def fly_down(self):
		self.y += self.down_velocity
		self.down_velocity += self.gravity

	def get_rect(self):
		return pygame.Rect(self.x, self.y, self.width, self.height)

class Tube:
	def __init__(self, x):
		self.x = x
		self.width = TUBE_WIDTH
		self.height = randint(100, HEIGHT // 2 + 20)
		self.gate_height = gate_height
		self.pipe_interval = pipe_interval
		self.velocity = TUBE_VELOCITY
		self.passed = False

# init object
bird = Bird(BIRD_X, bird_y)
tubes = [
	Tube(tube1_x),
	Tube(tube2_x),
	Tube(tube3_x)
]

# --- Variable caculate ---
score = 0
font = pygame.font.SysFont("sans", 20)
# is program continue?
pausing = False

while running:
	clock.tick(60)  # fps 

	# Draw background
	screen.blit(background_image, (0, 0))

	# Draw score txt
	score_txt = font.render("Score: " + str(score), True, TEXT_COLOR)
	screen.blit(score_txt, (10, 10))


	# Check collide with sky and base
	if bird.y <= 0 or bird.y + bird.height >= HEIGHT:
		pausing = True

	if not pausing:
		bird.fly_down()

	# Draw tube
	for tube in tubes:
		# Draw tube
		tube_rect = pygame.draw.rect(screen, TUBE_COLOR, (tube.x, 0, tube.width, tube.height))
		# Draw tube inverse
		tube_rect_inv = pygame.draw.rect(screen, TUBE_COLOR, (tube.x, tube.height + tube.gate_height, tube.width, HEIGHT - tube.height - tube.gate_height))

		# Move tube to the left
		if not pausing:
			tube.x -= tube.velocity

		# check collision
		for obj in [tube_rect, tube_rect_inv]:
			bird_rect = bird.get_rect()
			if bird_rect.colliderect(obj):
				pausing = True

		# Generate new tubes
		if tube.x <= -tube.width:
			tube.x += len(tubes) * tube.pipe_interval
			tube.height = randint(100, HEIGHT // 2 + 20)
			tube.passed = False		# Not plus score

		# update score and check first pass
		if tube.x + tube.width <= bird.x and not tube.passed:
			score += 1
			tube.passed = True

	# Draw bird
	bird_rect = screen.blit(bird.image, (bird.x, bird.y))

	if pausing:
		game_over_txt = font.render("Game over, score:" + str(score), True, NEON_PINK)
		screen.blit(game_over_txt, (WIDTH // 2 - 110, 200))
		press_space_txt = font.render("Press space to continue", True, NEON_CYAN)
		screen.blit(press_space_txt, (WIDTH // 2 - 110, 240))
		
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			# Quit the program
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				if pausing:
					bird.y = bird_y
					bird.down_velocity = 0
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