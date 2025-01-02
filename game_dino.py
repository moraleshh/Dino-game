import pygame
import os
import random

# Inisialisasi Pygame
pygame.init()

# Ukuran layar
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Kecepatan permainan
GAME_SPEED = 5

# Membuat layar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jump Dino")

# Memuat gambar
dino_image = pygame.image.load("kotak1.png")
cactus_image = pygame.image.load("kaktus2.png")

dino_width, dino_height = dino_image.get_size()
cactus_width, cactus_height = cactus_image.get_size()

pygame.font.init()
font = pygame.font.Font(None, 35)
lose1 = font.render('PLAYER 1 LOSE!', True, (180, 0, 0))

# Kelas Dino
class Dino:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT - dino_height - 10
        self.jump = False
        self.jump_vel = -15
        self.gravity = 1
        self.vel_y = 0

    def update(self):
        if self.jump:
            self.vel_y += self.gravity
            self.y += self.vel_y
            if self.y >= SCREEN_HEIGHT - dino_height - 10:
                self.y = SCREEN_HEIGHT - dino_height - 10
                self.jump = False
                self.vel_y = 0

    def draw(self, screen):
        screen.blit(dino_image, (self.x, self.y))

# Kelas Kaktus
class Cactus:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.y = SCREEN_HEIGHT - cactus_height - 10

    def update(self):
        self.x -= GAME_SPEED
        if self.x < -cactus_width:
            self.x = SCREEN_WIDTH + random.randint(0, 200)
            return True
        return False

    def draw(self, screen):
        screen.blit(cactus_image, (self.x, self.y))

# Fungsi utama permainan
def main():
    clock = pygame.time.Clock()
    run = True
    game_over = False
    score = 0

    dino = Dino()
    cactus = Cactus()

    while run:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not dino.jump and not game_over:
                    dino.jump = True
                    dino.vel_y = dino.jump_vel
                if event.key == pygame.K_r and game_over:
                    # Reset game
                    game_over = False
                    score = 0
                    dino = Dino()
                    cactus = Cactus()

        if not game_over:
            #Update objek
            dino.update()
            if cactus.update():
                score += 1

            # Deteksi tabrakan
            if (cactus.x < dino.x + dino_width and
                cactus.x + cactus_width > dino.x and
                cactus.y < dino.y + dino_height and
                cactus.y + cactus_height > dino.y):
                game_over = True

        # Gambar objek
        dino.draw(screen)
        cactus.draw(screen)

        # Tampilkan skor
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        if game_over:
            screen.blit(lose1, (200, 200))
            reset_text = font.render("Press 'R' to Reset", True, BLACK)
            screen.blit(reset_text, (200, 250))

        # Update layar    
        pygame.display.update()
        clock.tick(50)

    pygame.quit()

if __name__ == "__main__":
    main()
