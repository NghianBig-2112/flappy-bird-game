import pygame
import random
from config import *
from brain import NeuralBrain

class Bird:
	def __init__(self, y, image, brain=None):
		self.x = BIRD_X
		self.y = y
		self.velocity = 0
		self.flap = FLAP_VELOCITY
		self.image = image

        # brain
        self.brain = brain

		# --- GA attributes ---
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

    def think_and_act(self, inputs):
        if self.brain is not None:
            output = self.brain.predict(inputs)
            if output > 0.45 and self.velocity > 0:
                self.fly_up()


class Tube:
	def __init__(self, x, image_down, image_top):
		self.x = x
		self.y = random.randint(int(SCREEN_HEIGHT  * 0.3), int(SCREEN_HEIGHT  * 0.6))
		self.tube_image_down = image_down
		self.tube_image_top = image_top
		self.passed = False

    def update(self):
        self.x -= TUBE_VELOCITY

    def get_rect(self):
        top_rect = pygame.Rect(self.x, self.y - TUBE_HEIGHT, TUBE_WIDTH, TUBE_HEIGHT)
        down_rect = pygame.Rect(self.x, self.y + GATE_HEIGHT, TUBE_WIDTH, TUBE_HEIGHT)
        return top_rect, down_rect

# Get feature information of bird
def get_inputs(bird, tube):
	# index of bird
	bird_y_center = bird.y + BIRD_HEIGHT // 2
	# bird velocity
	bird_velo = bird.velocity
	# distance bird to nearest tube
	dis_nearest_tube = tube.x - (bird.x + BIRD_WIDTH)
	# distance to top and bottum tube
	dis_top_tube = bird.y - tube.y
	dis_buttom_tube = (tube.y + GATE_HEIGHT) - (bird.y + BIRD_HEIGHT)

	return [
		bird_y_center / SCREEN_HEIGHT,
		bird_velo / 10.0,
		dis_nearest_tube / SCREEN_WIDTH,
		dis_top_tube / SCREEN_HEIGHT,
		dis_buttom_tube / SCREEN_HEIGHT
	]