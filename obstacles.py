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

# ---------------- בור קולה ---------
class Cola_pit:
    def __init__(self,x,y):
        self.rect =  pygame.Rect(x, y,70 ,150)


    def draw(self,offset_x):
        # pygame.draw.rect(screen, RED, (self.rect.x - offset_x, self.rect.y, self.rect.width, self.rect.height))
        screen.blit(cola_pit_img, (self.rect.x - offset_x, self.rect.y-40))

#--------PLATFORM------
class Platform:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,400,100)

    def draw(self,offset_x):
        screen.blit(platform_img,(self.rect.x - offset_x, self.rect.y))