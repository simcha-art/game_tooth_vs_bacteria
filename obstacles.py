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

# ---------------- COLA ----------------
class Cola:
    def __init__(self):
        # המיקום: 520 כדי שיהיה מתחת לרצפה (שהיא בדרך כלל ב-500)
        self.rect = pygame.Rect(350, 520, 120, 80)
        self.color = (60, 30, 0) # צבע חום קולה

    def update(self, player, game_state):
        # בדיקת התנגשות עם השחקן שמישהו אחר יצר
        if player.rect.colliderect(self.rect):
            # מוריד ניקוד במקום להרוג (hp=0)
            if game_state['score'] > 0:
                game_state['score'] -= 1
            player.speed = 1  # האטה בגלל הדביקות
        else:
            player.speed = 5  # מהירות רגילה מחוץ לבור

    def draw(self, screen, offset_x):
        # כאן קורה הקסם של הציור עם ה-offset
        pygame.draw.rect(screen, self.color, (self.rect.x - offset_x, self.rect.y, self.rect.width, self.rect.height))