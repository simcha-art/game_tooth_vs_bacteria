import pygame
pygame.init()
# צבעים
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BROWN = (120, 70, 20)

#כוח המשיכה
gravity = 0.8

# רמה גדולה יותר מהמסך
LEVEL_WIDTH = 4000
LEVEL_HEIGHT = 600

# ---------------- מסך ומשאבים ----------------
WIDTH, HEIGHT = 800, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tooth Defender")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)


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
