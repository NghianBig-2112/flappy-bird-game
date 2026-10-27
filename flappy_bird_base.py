import pygame
from random import randint

# --- Color ---
TUBE_COLOR  = (56, 240, 43)
TEXT_COLOR  = (235, 240, 255)

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

# --- Background images ---
background_image = pygame.image.load("assets/background-day.png").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

bird_image = pygame.image.load("assets/yellowbird-midflap.png").convert_alpha()
bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT))

# Tube down
tube_image_down = pygame.image.load("assets/pipe-green.png").convert_alpha()
tube_image_down = pygame.transform.scale(tube_image_down, (TUBE_WIDTH, TUBE_HEIGHT))
# Tueb top
tube_image_top = pygame.transform.flip(tube_image_down, False, True)

# Gameover
gameover_image = pygame.image.load("assets/gameover.png").convert_alpha()

class Bird:
	def __init__(self, y):
		self.x = BIRD_X
		self.y = y
		self.velocity = bird_velocity
		self.flap = FLAP_VELOCITY
		self.image = bird_image

		# --- GA attributes ---
		self.chromosome = [uniform(-2, 2) for i in range(6)]	# gene bird
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

class Tube:
	def __init__(self, x):
		self.x = x
		self.y = randint(int(HEIGHT * 0.3), int(HEIGHT * 0.7))
		self.tube_image_down = tube_image_down
		self.tube_image_top = tube_image_top
		self.passed = False

# init object
bird = Bird(bird_y)
tubes = [
	Tube(tube1_x),
	Tube(tube2_x),
	Tube(tube3_x)
]

# --- Variable caculate ---
score = 0
font = pygame.font.SysFont("sans", 35)
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
	if bird.y <= 0 or bird.y + BIRD_HEIGHT >= HEIGHT:
		pausing = True

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

		# check collision
		for obj in [tube_rect_top, tube_rect_down]:
			bird_rect = bird.get_rect()
			if bird_rect.colliderect(obj):
				pausing = True

		# Generate new tubes
		if tube.x <= -TUBE_WIDTH:
			tube.x += len(tubes) * TUBE_INTERVAL
			tube.y = randint(int(HEIGHT * 0.3), int(HEIGHT * 0.7))
			tube.passed = False		# Not plus score

		# update score and check first pass
		if tube.x + TUBE_WIDTH <= bird.x and not tube.passed:
			score += 1
			tube.passed = True

	# Draw bird
	bird_rect = screen.blit(bird.image, (bird.x, bird.y))

	if pausing:
		screen.blit(gameover_image, (100, 100))
		game_over_txt = font.render("Game over, score:" + str(score), True, TEXT_COLOR)
		screen.blit(game_over_txt, (WIDTH // 2 - 110, 200))
		press_space_txt = font.render("Press space to continue", True, TEXT_COLOR)
		screen.blit(press_space_txt, (WIDTH // 2 - 110, 240))
		
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