import pygame
import random
from abc import ABC, abstractmethod
from settings import *

class BaseBacteria(ABC):
    def __init__(self, x, y, width=100, height=100, speed=2, damage=10):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.damage = damage
        # משתנה שעוזר לנו לדעת לאיזה כיוון החיידק מסתכל (לצורך הציור)
        self.facing_right = random.choice([True, False])
        # תמונות (ברירת מחדל - רגיל)
        self.img_right = germ_img_right
        self.img_left = germ_img_left


    @abstractmethod
    def move(self, target_rect=None):
        """
        פונקציה אבסטרקטית. כל חיידק שיירש ממחלקת הבסיס *חייב*
        לממש את הפונקציה הזו בעצמו עם ההיגיון שלו.
        """
        pass

    def draw(self, offset_x):
        if self.facing_right:
            screen.blit(self.img_right, (self.rect.x - offset_x, self.rect.y))
        else:
            screen.blit(self.img_left, (self.rect.x - offset_x, self.rect.y))

# ---------------- 1. חיידק רגיל (מהיר, לא עוקב) ----------------
class RegularBacteria(BaseBacteria):
    def __init__(self, x, y):
        # קורא ל-init של מחלקת הבסיס, עם מהירות גבוהה (4) ונזק רגיל (10)
        super().__init__(x, y, speed=4, damage=10)
        self.current_speed = self.speed if self.facing_right else -self.speed

    def move(self, target_rect=None):
        self.rect.x += self.current_speed

        # שינוי כיוון כשהוא פוגע בקצוות המסך
        if self.rect.left < 0 or self.rect.right > LEVEL_WIDTH:
            self.current_speed *= -1
            self.facing_right = self.current_speed > 0




# ---------------- 2. חיידק עוקב (איטי, רודף אחרי השן) ----------------
class TrackerBacteria(BaseBacteria):
    def __init__(self, x, y):
        # מהירות נמוכה (1.5)
        super().__init__(x, y, width=120, height=120, speed=2, damage=10)
        self.img_right = tracker_img_right
        self.img_left = tracker_img_left

    def move(self, target_rect):
        # אם יש מטרה (השן), נזוז לכיוונה
        if target_rect:
            if target_rect.centerx > self.rect.centerx:
                self.rect.x += self.speed
                self.facing_right = True
            elif target_rect.centerx < self.rect.centerx:
                self.rect.x -= self.speed
                self.facing_right = False


# ---------------- 3. חיידק אביר (כבד, מוריד הרבה חיים) ----------------
class KnightBacteria(BaseBacteria):
    def __init__(self, x, y):

        # מהירות בינונית (2), אבל נזק כפול (20)
        super().__init__(x, y, speed=2, damage=20)
        self.img_right = knight_img_right
        self.img_left = knight_img_left
        self.current_speed = self.speed if self.facing_right else -self.speed

    def move(self, target_rect=None):
        # מתנהג כמו חיידק רגיל מבחינת תנועה, אבל אפשר להוסיף פה התנהגות שונה בעתיד
        self.rect.x += self.current_speed
        if self.rect.left < 0 or self.rect.right > LEVEL_WIDTH:
            self.current_speed *= -1
            self.facing_right = self.current_speed > 0


class AcidDrop:
    def __init__(self, x, y, facing_right):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.speed = 6 if facing_right else -6
        self.damage = 10  # מחסיר 10 חיים במקום 5

    def move(self):
        self.rect.x += self.speed

    def draw(self, offset_x):
        # כרגע מצויר כריבוע ירוק, אפשר להחליף בתמונה
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x - offset_x, self.rect.y, 10, 10))


class ShooterBacteria(BaseBacteria):
    def __init__(self, x, y):
        self.img_right = shooter_img_right
        self.img_left = shooter_img_left
        super().__init__(x, y, speed=2, damage=5)  # מגע רגיל עושה מעט נזק (5)
        self.shoot_cooldown = 0
        self.projectiles = []

    def move(self, target_rect):
        # נניח שהוא תמיד מסתכל לכיוון השחקן אבל נשאר במקום או זז לאט
        if target_rect:
            self.facing_right = target_rect.centerx > self.rect.centerx

            # מערכת ירייה (Cooldown) כדי שלא יירו 60 קליעים בשנייה
            if self.shoot_cooldown > 0:
                self.shoot_cooldown -= 1
            else:
                # יורה קליע
                self.projectiles.append(AcidDrop(self.rect.centerx, self.rect.centery, self.facing_right))
                self.shoot_cooldown = 60  # יורה כל 60 פריימים (נניח שנייה אחת)

        # מעדכן את הקליעים שלו
        for proj in self.projectiles:
            proj.move()

    def draw(self, offset_x):
        # מצייר את החיידק
        super().draw(offset_x)
        # מצייר גם את הקליעים שלו
        for proj in self.projectiles:
            proj.draw(offset_x)

