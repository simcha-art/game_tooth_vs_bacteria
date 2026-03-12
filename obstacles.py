import pygame
import random
from settings import *

# ---------------- CANDY ----------------
class Candy:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, LEVEL_WIDTH), 0, 20, 20)
        self.speed = 3

    def move(self):
        self.rect.y += self.speed

    def draw(self, offset_x):
        screen.blit(candy_img,(self.rect.x - offset_x, self.rect.y))