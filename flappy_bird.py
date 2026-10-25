import pygame
from random import randint

# --- Color ---
TUBE_COLOR  = (30, 170, 160)    # thân cột (teal)
TEXT_COLOR  = (235, 240, 255)   # chữ chính (trắng ngả xanh)
NEON_PINK   = (255, 60, 170)    # chữ Game over
NEON_CYAN   = (60, 230, 255)    # chữ hướng dẫn

# --- Screen ---
WIDTH, HEIGHT = 480, 640
FPS = 60

# --- Init program ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
running = True
clock = pygame.time.Clock()


# --- Bird ---
BIRD_WIDTH, BIRD_HEIGHT = 40, 28
BRID_X = WIDTH // 4
bird_y = HEIGHT // 3
GRAVITY = 0.5

bird_drop_velocity = 0	# speed down of bird
JUMP_VELOCITY = 8	# speed up

# --- Tube ---
TUBE_VELOCITY = 3   # Speed of tube
TUBE_WIDTH = 50
TUBE_GAP = 150	# distance of 2 tubes (tube and tube_inv)

tube1_x = WIDTH + 50
tube2_x = WIDTH + 250
tube3_x = WIDTH + 450

tube1_height = randint(50, HEIGHT // 2)
tube2_height = randint(50, HEIGHT // 2)
tube3_height = randint(50, HEIGHT // 2)

tube1_pass = False
tube2_pass = False
tube3_pass = False

# --- Background images ---
background_image = pygame.image.load("assets/Game_Objects/background_and_road.png").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

bird_image = pygame.image.load("assets/Game_Objects/yellowbird-midflap.png").convert_alpha()
bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT))

sand_image = pygame.image.load("assets/Game_Objects/base.png").convert_alpha()
sand_image = pygame.transform.scale(sand_image, (WIDTH, HEIGHT // 5))

sky_image = pygame.image.load("assets/Game_Objects/pixel-sky.png").convert_alpha()
sky_image = pygame.transform.scale(sky_image, (WIDTH, HEIGHT // 5))

score = 0
font = pygame.font.SysFont("sans", 20)

pausing = False
while running:
	clock.tick(FPS)  # fps 

	# Draw background
	screen.blit(background_image, (0, 0))

	# draw sky
	sky_rect = screen.blit(sky_image, (0, 0))

	# Draw tube
	tube1_rect = pygame.draw.rect(screen, TUBE_COLOR, (tube1_x, 0, TUBE_WIDTH, tube1_height))
	tube2_rect = pygame.draw.rect(screen, TUBE_COLOR, (tube2_x, 0, TUBE_WIDTH, tube2_height))
	tube3_rect = pygame.draw.rect(screen, TUBE_COLOR, (tube3_x, 0, TUBE_WIDTH, tube3_height))

	# Draw tube inverse
	tube1_rect_inv = pygame.draw.rect(screen, TUBE_COLOR, (tube1_x, tube1_height + TUBE_GAP, TUBE_WIDTH, HEIGHT - tube1_height - TUBE_GAP))
	tube2_rect_inv = pygame.draw.rect(screen, TUBE_COLOR, (tube2_x, tube2_height + TUBE_GAP, TUBE_WIDTH, HEIGHT - tube2_height - TUBE_GAP))
	tube3_rect_inv = pygame.draw.rect(screen, TUBE_COLOR, (tube3_x, tube3_height + TUBE_GAP, TUBE_WIDTH, HEIGHT - tube3_height - TUBE_GAP))


	# Move tube to the left
	tube1_x -= TUBE_VELOCITY
	tube2_x -= TUBE_VELOCITY
	tube3_x -= TUBE_VELOCITY

	# draw sand
	sand_rect = screen.blit(sand_image, (0, 531))

	# draw bird
	bird_rect = screen.blit(bird_image, (BRID_X, bird_y))

	# Bird falls
	bird_y += bird_drop_velocity
	bird_drop_velocity += GRAVITY
	
	# Generate new tubes
	if tube1_x < -TUBE_WIDTH:
		tube1_x = WIDTH + 50
		tube1_height = randint(50, HEIGHT // 2)
		tube1_pass = False
	if tube2_x < -TUBE_WIDTH:
		tube2_x = WIDTH + 50
		tube2_height = randint(50, HEIGHT // 2)
		tube2_pass = False
	if tube3_x < -TUBE_WIDTH:
		tube3_x = WIDTH + 50
		tube3_height = randint(50, HEIGHT // 2)
		tube3_pass = False

	# # draw score txt
	score_txt = font.render("Score: " + str(score), True, TEXT_COLOR)
	screen.blit(score_txt, (10, 10))

	# update score
	if tube1_x + TUBE_WIDTH <= BRID_X and tube1_pass == False:
		score += 1	
		tube1_pass = True
	if tube2_x + TUBE_WIDTH <= BRID_X and tube2_pass == False:
		score += 1	
		tube2_pass = True
	if tube3_x + TUBE_WIDTH <= BRID_X and tube3_pass == False:
		score += 1
		tube3_pass = True

	# check collision
	for tube in [tube1_rect, tube2_rect, tube3_rect, tube1_rect_inv, tube2_rect_inv, tube3_rect_inv, sand_rect]:
		if bird_rect.colliderect(tube):
			pausing = True
			TUBE_VELOCITY = 0	
			bird_drop_velocity = 0
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
				# reset
				if pausing:
					bird_y = HEIGHT // 3
					TUBE_VELOCITY = 3
					tube1_x = WIDTH + 50
					tube2_x = WIDTH + 250
					tube3_x = WIDTH + 450
					score = 0
					pausing = False

				bird_drop_velocity = 0
				bird_drop_velocity -= JUMP_VELOCITY

	pygame.display.flip()

pygame.quit()