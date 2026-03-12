import pygame
from settings import *
from pro_main import *
# ---------------- BULLET ----------------
class Bullet:
    def __init__(self, x, y,direction):
        self.rect = pygame.Rect(x, y, 12, 6)
        self.start_point = x
        self.range = 200
        self.speed = 5
        self.facing_right = direction


    def move(self):
        if self.facing_right:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

    def out_of_range(self):
        return abs(self.rect.x - self.start_point) > self.range

    def draw(self, offset_x):
        if self.facing_right:
            screen.blit(bullets_img_right,((self.rect.x - offset_x)-50, self.rect.y - 25))
        else:
            screen.blit(bullets_img_left,((self.rect.x - offset_x)-120, self.rect.y - 25))

