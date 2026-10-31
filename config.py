import pygame

# --- Screen size ---
SCREEN_WIDTH = 432
SCREEN_HEIGHT = 768
FPS = 60

# --- Color ---
TEXT_COLOR  = (235, 240, 255)
NEON_PINK   = (255, 60, 170)    # chữ Game over
NEON_CYAN   = (60, 230, 255)    # chữ hướng dẫn

# --- Physical of Bird ---
BIRD_WIDTH = 51
BIRD_HEIGHT = 36
BIRD_X = SCREEN_WIDTH // 5
BIRD_START_Y = SCREEN_HEIGHT // 2
GRAVITY = 0.5
FLAP_VELOCITY = 7 	# speed up of bird

# --- Tube ---
TUBE_WIDTH = 78 
TUBE_HEIGHT = 480
TUBE_VELOCITY = 2   # Speed of tube move to the left
GATE_HEIGHT = 100	# distance of 2 tubes (tube and tube_inv)
TUBE_INTERVAL = 250	# time next tube appear

# -- Setting of genetic algorithm
POP_SIZE = 30
NUM_INPUTS = 5     # number input of no ron
MUTATION_RATE = 0.1
MUTATION_SIGMA = 0.3
