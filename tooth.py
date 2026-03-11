import pygame
from settings import *
# ---------------- PLAYER ----------------
class Tooth:
    def __init__(self):
        self.rect = pygame.Rect(100, 400, 60, 60)
        self.vel_y = 0
        self.hp = 100
        self.on_ground = False
        self.facing_right = True

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
            self.facing_right = True
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -15
            self.on_ground = False

        self.vel_y += gravity
        self.rect.y += self.vel_y

        if self.rect.bottom >= 500:
            self.rect.bottom = 500
            self.vel_y = 0
            self.on_ground = True

        # לא לצאת מגבולות העולם
        self.rect.x = max(0, min(LEVEL_WIDTH - self.rect.width, self.rect.x))

    def draw(self, offset_x):
        if self.facing_right:
            screen.blit(tooth_img_right, (self.rect.x - offset_x, self.rect.y))
        else:
            screen.blit(tooth_img_left, (self.rect.x - offset_x, self.rect.y))

