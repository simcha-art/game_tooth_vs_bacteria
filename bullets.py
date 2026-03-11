import pygame
from settings import *
from pro_main import *
# ---------------- BULLET ----------------
class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 12, 6)
        self.speed = 10
        self.facing_right = True

    def move(self):
        if player.facing_right:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

    def draw(self, offset_x):
        pygame.draw.rect(screen, (0, 200, 255), (self.rect.x - offset_x, self.rect.y, self.rect.width, self.rect.height))
