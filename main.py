import pygame
import math
import numpy as np
import random
from random import randint
import json
import os

# --- Hàm đọc bộ gene tốt nhất đã lưu ---
def load_best_bird(filename="best_bird.json"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            chromosome = json.load(f)
        print(f"Đã nạp thành công bộ gene vô địch từ: {filename}")
        return chromosome
    print(f"Không tìm thấy file {filename}, AI sẽ dùng gene ngẫu nhiên!")
    return [random.uniform(-3, 3) for _ in range(6)]

# --- Color ---
TUBE_COLOR  = (56, 240, 43)
TEXT_COLOR  = (235, 240, 255)
NEON_CYAN   = (60, 230, 255)    # Màu cho người chơi
NEON_PINK   = (255, 60, 170)    # Màu cho AI

# --- Screen ---
WIDTH, HEIGHT = 432, 768

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird - Solo với AI")
running = True
clock = pygame.time.Clock()

# --- Bird ---
BIRD_WIDTH, BIRD_HEIGHT = 51, 36
BIRD_X = WIDTH // 5
bird_y = HEIGHT // 2
GRAVITY = 0.5
FLAP_VELOCITY = 7 

# --- Tube ---
TUBE_WIDTH, TUBE_HEIGHT = 78, 480
TUBE_VELOCITY = 2
GATE_HEIGHT = 170
TUBE_INTERVAL = 250
tube1_x = WIDTH
tube2_x = tube1_x + TUBE_INTERVAL
tube3_x = tube2_x + TUBE_INTERVAL

# --- Hình ảnh ---
background_image = pygame.image.load("assets/background-day.png").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Ảnh chim Người chơi (Màu vàng gốc)
player_bird_image = pygame.image.load("assets/yellowbird-midflap.png").convert_alpha()
player_bird_image = pygame.transform.scale(player_bird_image, (BIRD_WIDTH, BIRD_HEIGHT))

# Ảnh chim AI (Dùng chim xanh - Bluebird)
ai_bird_image = pygame.image.load("assets/bluebird-midflap.png").convert_alpha()
ai_bird_image = pygame.transform.scale(ai_bird_image, (BIRD_WIDTH, BIRD_HEIGHT))

# Ống
tube_image_down = pygame.image.load("assets/pipe-green.png").convert_alpha()
tube_image_down = pygame.transform.scale(tube_image_down, (TUBE_WIDTH, TUBE_HEIGHT))
tube_image_top = pygame.transform.flip(tube_image_down, False, True)

gameover_image = pygame.image.load("assets/gameover.png").convert_alpha()

# --- Lớp Chim ---
class Bird:
    def __init__(self, y, image, is_ai=False):
        self.x = BIRD_X
        self.y = y
        self.velocity = 0
        self.flap = FLAP_VELOCITY
        self.image = image
        self.is_ai = is_ai
        self.alive = True
        self.score = 0
        self.chromosome = [0.0] * 6

    def fly_up(self):
        self.velocity = 0
        self.velocity -= self.flap

    def fly_down(self):
        self.y += self.velocity
        self.velocity += GRAVITY

    def get_rect(self):
        return pygame.Rect(self.x, self.y, BIRD_WIDTH, BIRD_HEIGHT)

    # Não của chim AI
    def think(self, inputs):
        y = 0
        for i in range(len(inputs)):
            y += self.chromosome[i] * inputs[i]
        y += self.chromosome[-1]

        output = 1 / (1 + np.exp(-y))
        if output > 0.45 and self.velocity > 0:
            self.fly_up()

# --- Lớp Ống ---
class Tube:
    def __init__(self, x):
        self.x = x
        self.y = randint(int(HEIGHT * 0.3), int(HEIGHT * 0.6))
        self.tube_image_down = tube_image_down
        self.tube_image_top = tube_image_top
        self.passed = False

# --- Hàm tính toán đầu vào cho AI ---
def get_inputs(bird, tube):
    bird_y_center = bird.y + BIRD_HEIGHT // 2
    bird_velo = bird.velocity
    dis_nearest_tube = tube.x - (bird.x + BIRD_WIDTH // 2)
    dis_top_tube = bird_y_center - tube.y
    dis_buttom_tube = (tube.y + GATE_HEIGHT) - bird_y_center

    return [
        bird_y_center / HEIGHT,
        bird_velo / 10,
        dis_nearest_tube / WIDTH,
        dis_top_tube / HEIGHT,
        dis_buttom_tube / HEIGHT
    ]

# --- Khởi tạo 2 đấu thủ ---
bird_player = Bird(bird_y, player_bird_image, is_ai=False)
bird_ai = Bird(bird_y, ai_bird_image, is_ai=True)
bird_ai.chromosome = load_best_bird("best_bird.json")  # Nạp gene vô địch cho AI

tubes = [Tube(tube1_x), Tube(tube2_x), Tube(tube3_x)]

font = pygame.font.SysFont("sans", 24, bold=True)
small_font = pygame.font.SysFont("sans", 16, bold=True)
pausing = False

# --- Vòng lặp chính ---
while running:
    clock.tick(60)

    # 1. Vẽ nền
    screen.blit(background_image, (0, 0))

    # 2. Tìm ống gần nhất phía trước
    nearest_tube = None
    for tube in tubes:
        if tube.x + TUBE_WIDTH >= BIRD_X:
            if nearest_tube is None or tube.x < nearest_tube.x:
                nearest_tube = tube

    # 3. Cập nhật AI
    if bird_ai.alive and not pausing:
        if nearest_tube:
            inputs = get_inputs(bird_ai, nearest_tube)
            bird_ai.think(inputs)
        bird_ai.fly_down()
        if bird_ai.y <= 0 or bird_ai.y + BIRD_HEIGHT >= HEIGHT:
            bird_ai.alive = False

    # 4. Cập nhật Người chơi
    if bird_player.alive and not pausing:
        bird_player.fly_down()
        if bird_player.y <= 0 or bird_player.y + BIRD_HEIGHT >= HEIGHT:
            bird_player.alive = False

    # 5. Nếu cả 2 đều chết -> Tạm dừng ván đấu
    if not bird_player.alive and not bird_ai.alive:
        pausing = True

    # 6. Vẽ và di chuyển ống
    for tube in tubes:
        tube_rect_top = screen.blit(tube_image_top, (tube.x, tube.y - TUBE_HEIGHT))
        tube_rect_down = screen.blit(tube_image_down, (tube.x, tube.y + GATE_HEIGHT))

        if not pausing:
            tube.x -= TUBE_VELOCITY

        # Kiểm tra va chạm ống
        for b in [bird_player, bird_ai]:
            if b.alive:
                rect = b.get_rect()
                if rect.colliderect(tube_rect_top) or rect.colliderect(tube_rect_down):
                    b.alive = False

        # Cập nhật điểm
        if tube.x + TUBE_WIDTH <= BIRD_X and not tube.passed:
            if bird_player.alive:
                bird_player.score += 1
            if bird_ai.alive:
                bird_ai.score += 1
            tube.passed = True

        # Tái tạo ống mới
        if tube.x <= -TUBE_WIDTH:
            tube.x += len(tubes) * TUBE_INTERVAL
            tube.y = randint(int(HEIGHT * 0.3), int(HEIGHT * 0.6))
            tube.passed = False

    # 7. Vẽ chim và nhãn tên trên đầu
    if bird_ai.alive:
        screen.blit(bird_ai.image, (bird_ai.x, bird_ai.y))
        tag_ai = small_font.render("AI", True, NEON_PINK)
        screen.blit(tag_ai, (bird_ai.x + 15, bird_ai.y - 18))
    if bird_player.alive:
        screen.blit(bird_player.image, (bird_player.x, bird_player.y))
        tag_you = small_font.render("YOU", True, NEON_CYAN)
        screen.blit(tag_you, (bird_player.x + 10, bird_player.y - 18))


    # 8. Bảng điểm thi đấu song song
    player_score_txt = font.render(f"YOU: {bird_player.score}", True, NEON_CYAN)
    ai_score_txt     = font.render(f"AI: {bird_ai.score}", True, NEON_PINK)
    screen.blit(player_score_txt, (20, 20))
    screen.blit(ai_score_txt, (WIDTH - 120, 20))

    # 9. Màn hình Game Over & Phân định Thắng/Thua
    if pausing:
        screen.blit(gameover_image, (WIDTH // 2 - 96, 180))
        
        # Xác định ai thắng
        if bird_player.score > bird_ai.score:
            result_txt = font.render("YOU WIN!", True, NEON_CYAN)
        elif bird_player.score < bird_ai.score:
            result_txt = font.render("AI WINS!", True, NEON_PINK)
        else:
            result_txt = font.render("DRAW (HÒA)!", True, TEXT_COLOR)

        screen.blit(result_txt, (WIDTH // 2 - 80, 250))
        press_space_txt = small_font.render("Press SPACE to play again", True, TEXT_COLOR)
        screen.blit(press_space_txt, (WIDTH // 2 - 100, 300))

    # 10. Sự kiện phím bấm
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if pausing:
                    # Reset lại cả 2 đấu thủ và cột
                    bird_player = Bird(bird_y, player_bird_image, is_ai=False)
                    bird_ai = Bird(bird_y, ai_bird_image, is_ai=True)
                    bird_ai.chromosome = load_best_bird("best_bird.json")
                    tubes = [Tube(tube1_x), Tube(tube2_x), Tube(tube3_x)]
                    pausing = False
                else:
                    if bird_player.alive:
                        bird_player.fly_up()

    pygame.display.flip()

pygame.quit()