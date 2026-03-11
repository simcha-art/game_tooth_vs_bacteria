import pygame
from settings import *
from pro_main import *
# ---------------- BULLET ----------------
class Bullet:
    def __init__(self, x, y,direction):
        self.rect = pygame.Rect(x, y, 12, 6)
        self.start_point = x
        self.range = 200
        self.speed = 10
        self.facing_right = direction


    def move(self):
        if self.facing_right:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

    def out_of_range(self):
        return abs(self.rect.x - self.start_point) > self.range

    def draw(self, offset_x):
        pygame.draw.rect(screen, (0, 200, 255), (self.rect.x - offset_x, self.rect.y, self.rect.width, self.rect.height))
