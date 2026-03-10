import pygame
import random
import json
import sys

pygame.init()

# ---------------- מסך ומשאבים ----------------
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tooth Defender")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# צבעים
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BROWN = (120, 70, 20)

gravity = 0.8

# רמה גדולה יותר מהמסך
LEVEL_WIDTH = 4000
LEVEL_HEIGHT = 600

offset_x = 0  # המצלמה

# טעינת תמונות

floor_img = pygame.image.load("static/floor.png")

tooth_img_right = pygame.image.load("static/tooth_right.png")
tooth_img_right = pygame.transform.scale(tooth_img_right, (60, 60))

tooth_img_left = pygame.image.load("static/tooth_left.png")
tooth_img_left = pygame.transform.scale(tooth_img_left, (60, 60))

germ_img_right = pygame.image.load("static/germ_right.png")
germ_img_right = pygame.transform.scale(germ_img_right, (50, 50))

germ_img_left = pygame.image.load("static/germ_left.png")
germ_img_left = pygame.transform.scale(germ_img_left, (50, 50))

candy_img = pygame.image.load("static/candy.png")
candy_img = pygame.transform.scale(candy_img,(40,40))
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

# ---------------- CANDY ----------------
class Candy:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, LEVEL_WIDTH), 0, 20, 20)
        self.speed = 3

    def move(self):
        self.rect.y += self.speed

    def draw(self, offset_x):
        screen.blit(candy_img,(self.rect.x - offset_x, self.rect.y))

# ---------------- SCORE SAVE ----------------
def save_score(score):
    try:
        with open("scores.json", "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(score)
    data = sorted(data, reverse=True)[:5]

    with open("scores.json", "w") as f:
        json.dump(data, f)

# ---------------- RESET LEVEL ----------------
def reset_level(player, bacteria, bullets, candies):
    player.hp = 100
    player.rect.topleft = (100, 400)
    bullets.clear()
    candies.clear()
    bacteria[:] = [Bacteria(random.randint(300,4000),460) for b in range(10)]

# ---------------- MAIN GAME ----------------
player = Tooth()
bacteria = [Bacteria(random.randint(300,4000),460) for b in range(10)]
bullets = []
candies = []
score = 0
spawn_timer = 0
game_state = "playing"

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f and game_state == "playing":
                bullets.append(Bullet(player.rect.right, player.rect.centery))

    keys = pygame.key.get_pressed()

    if game_state == "playing":
        # תנועה
        player.move(keys)

        # עדכון מצלמה
        offset_x = player.rect.x - WIDTH // 2
        offset_x = max(0, min(LEVEL_WIDTH - WIDTH, offset_x))

        # ניהול סוכריות
        spawn_timer += 1
        if spawn_timer > 200:
            candies.append(Candy())
            spawn_timer = 0
        for c in candies:
            c.move()

        # חיידקים וקליעים
        for b in bacteria:
            b.move()
        for bullet in bullets:
            bullet.move()

        # פגיעות קליעים בחיידקים
        for bullet in bullets[:]:
            for b in bacteria[:]:
                if bullet.rect.colliderect(b.rect):
                    bullets.remove(bullet)
                    bacteria.remove(b)
                    score += 50
                    break

        # פגיעות השחקן
        for b in bacteria[:]:
            if player.rect.colliderect(b.rect):
                player.hp -= 10
                bacteria.remove(b)

        for s in candies[:]:
            if player.rect.colliderect(s.rect):
                player.hp -= 5
                candies.remove(s)

        # בור קולה
        cola_pit = pygame.Rect(350, 500, 120, 100)
        if player.rect.colliderect(cola_pit):
            player.hp = 0

        if player.hp <= 0:
            save_score(score)
            reset_level(player, bacteria, bullets, candies)
            score = 0

        # ציור המסך
        screen.fill((30, 30, 30))
        pygame.draw.rect(screen, BROWN, (0 - offset_x, 500, LEVEL_WIDTH, 100))  # רצפת המשחק
        pygame.draw.rect(screen, RED, (cola_pit.x - offset_x, cola_pit.y, cola_pit.width, cola_pit.height))
        player.draw(offset_x)
        for b in bacteria: b.draw(offset_x)
        for s in candies: s.draw(offset_x)
        for bullet in bullets: bullet.draw(offset_x)

        hp_text = font.render(f"HP: {player.hp}", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(hp_text, (20, 20))
        screen.blit(score_text, (20, 60))

    pygame.display.update()