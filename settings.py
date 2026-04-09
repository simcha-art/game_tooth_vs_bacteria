import pygame
from PIL.ImageOps import scale

pygame.init()
# צבעים
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BROWN = (120, 70, 20)
YELLOW = (255, 255, 80)
GREEN = (50, 250, 70)
LIGHT_BLUE = (180, 230, 255)
BLUE = (0, 0, 255)
PINK = (255, 180, 180)
PURPLE = (200, 20, 200)



#צבע רקע
GUM_PINK = (200, 80, 150)

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
floor_img = pygame.transform.scale(floor_img, (500, 426))
platform_img = pygame.transform.scale(floor_img,(400,300))

# ------------ TOOTH ----------------------

tooth_img_right = pygame.image.load("static/tooth_right.png")
tooth_img_right = pygame.transform.scale(tooth_img_right, (120, 120))
large_tooth_left = pygame.image.load("static/large_tooth_left.png")
tooth_img_left = pygame.image.load("static/tooth_left.png")
tooth_img_left = pygame.transform.scale(tooth_img_left, (120, 120))

# -------------- RegularBacteria -------------------

germ_img_right = pygame.image.load("static/germ_right.png")
germ_img_right = pygame.transform.scale(germ_img_right, (100, 100))

germ_img_left = pygame.image.load("static/germ_left.png")
germ_img_left = pygame.transform.scale(germ_img_left, (100, 100))

# ---------------- TRACKER ----------------
tracker_img_right = pygame.image.load("static/tracing_germ_right.png")
tracker_img_right = pygame.transform.scale(tracker_img_right, (120, 120))

tracker_img_left = pygame.image.load("static/tracing_germ_left.png")
tracker_img_left = pygame.transform.scale(tracker_img_left, (120, 120))


# ---------------- KNIGHT ----------------
knight_img_right = pygame.image.load("static/knight_right.png")
knight_img_right = pygame.transform.scale(knight_img_right, (120, 120))

knight_img_left = pygame.image.load("static/knight_left.png")
knight_img_left = pygame.transform.scale(knight_img_left, (120, 120))


# ---------------- SHOOTER ----------------
shooter_img_right = pygame.image.load("static/acid germ_right.png")
shooter_img_right = pygame.transform.scale(shooter_img_right, (140, 120))

shooter_img_left = pygame.image.load("static/acid germ_left.png")
shooter_img_left = pygame.transform.scale(shooter_img_left, (140, 120))

#---------------- JUMPER ------------------
jumper_img_right = pygame.image.load("static/jump bacteria.png")
jumper_img_right = pygame.transform.scale(jumper_img_right,(140,120))

jumper_img_left = pygame.image.load("static/jump bacteria left.png")
jumper_img_left = pygame.transform.scale(jumper_img_left,(140,120))

#---------------- CANDY --------------

candy_img = pygame.image.load("static/candy.png")
candy_img = pygame.transform.scale(candy_img,(40,40))

#-------------- GATE --------------------

gate_img = pygame.image.load("static/gate.png")
gate_img = pygame.transform.scale(gate_img,(200,200))


#תמונות של הבלונים
YELLO_BALLOON_IMG = pygame.image.load("static/yellow_balloon.png")
RED_BALLOON_IMG = pygame.image.load("static/red_balloon.png")
PURPLE_BALLOON_IMG = pygame.image.load("static/purple_balloon.png")
GREEN_BALLOON_IMG = pygame.image.load("static/green_balloon.png")
LIGHT_BLUE_BALLOON_IMG = pygame.image.load("static/light_blue_balloon.png")

bullets_img_right = pygame.image.load("static/paste.png")
bullets_img_right = pygame.transform.scale(bullets_img_right,(40,40))

bullets_img_left = pygame.image.load("static/paste_left.png")
bullets_img_left = pygame.transform.scale(bullets_img_left,(40,40))

cola_pit_img = pygame.image.load("static/cola_pit.png")
cola_pit_img = pygame.transform.scale(cola_pit_img,(150,200))
# ------טעינת צלילים-----
jump_sound = pygame.mixer.Sound("sounds/jumping.wav")
shot_sound = pygame.mixer.Sound("sounds/shot.wav")
game_over_sound=  pygame.mixer.Sound("sounds/game_over.wav")
player_hit_sound = pygame.mixer.Sound("sounds/player_hit.wav")
