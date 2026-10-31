import pygame

import math
import numpy as np
import random
import json

from config import *
from brain impor *
from entities import *
from genetic_algorithm import *

pygame.init()
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
running = True
clock = pygame.time.Clock()

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

# Create a population
population_bird = [Bird(BIRD_START_Y, bird_image, brain = NeuralBrain(num_inputs=NUM_INPUTS)) for _ in range(POP_SIZE)]
# --- Tube ---
tube1_x = SCREEN_WIDTH
tube2_x = tube1_x + TUBE_INTERVAL
tube3_x = tube2_x + TUBE_INTERVAL
tubes = [
	Tube(tube1_x),
	Tube(tube2_x),
	Tube(tube3_x)
]

# --- Init Genetic Algorithm
ga_model = genetic_algorithm.GeneticAlgorithm()
generation = 1

# --- Variable caculate ---
font = pygame.font.SysFont("sans", 20)
# is program continue?
pausing = False

while running:
	clock.tick(FPS)  # fps 
			
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
			bird.think_and_act(inputs)
			
		# Check collide with sky and base
		if bird.y <= 0 or bird.y + BIRD_HEIGHT >= SCREEN_HEIGHT:
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
			tube.y = random.randint(int(SCREEN_HEIGHT * 0.3), int(SCREEN_HEIGHT * 0.6))
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