import pygame
import random
from settings import *

# ---------------- BACTERIA ----------------
class Bacteria:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed = random.choice([-2, 2])

    def move(self):
        self.rect.x += self.speed
        if self.rect.left < 0 or self.rect.right > LEVEL_WIDTH:
            self.speed *= -1

    def draw(self, offset_x):
        if self.speed > 0:
            screen.blit(germ_img_right, (self.rect.x - offset_x, self.rect.y))
        else:
            screen.blit(germ_img_left, (self.rect.x - offset_x, self.rect.y))
