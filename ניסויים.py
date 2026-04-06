import pygame
import random
import sys

from bacterias import *
from tooth import *
from bullets import *
from settings import *
from obstacles import *
from screens import *
from data import *

pygame.init()
pygame.mixer.init()

# ---------------- GLOBALS ----------------
score = 0
spawn_timer = 0
level_game = 1
last_damage_time = 0
damage_delay = 500

game_state = "start"

start_screen = StartScreen()
game_over_screen = GameOverScreen()
victory_screen = VictoryScreen()
final_victory_screen = FinalVictoryScreen()

# ---------------- LEVEL LOADER ----------------

def load_level(level):
    global bacteria, player, bullets, candies, cola_pits, platforms, gate

    player = Tooth()
    bullets = []
    candies = []

    if level == 1:
        bacteria = [RegularBacteria(random.randint(300, 4000), 420) for _ in range(10)]
        cola_pits = [Cola_pit(955, 500), Cola_pit(1970, 500), Cola_pit(2970, 500)]
        platforms = [Platform(800, 200), Platform(1870, 200), Platform(2870, 200)]

    elif level == 2:
        bacteria = [RegularBacteria(random.randint(300, 4000), 420) for _ in range(20)]
        cola_pits = [Cola_pit(1200, 500), Cola_pit(2500, 500)]
        platforms = [Platform(1000, 250), Platform(2000, 150)]

    gate = Gate()

# טען שלב ראשון
load_level(level_game)

# ---------------- MAIN LOOP ----------------

while True:
    clock.tick(60)
    current_time = pygame.time.get_ticks()

    # -------- EVENTS --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if game_state == "start" and event.key == pygame.K_RETURN:
                game_state = "playing"

            elif game_state == "game_over" and event.key == pygame.K_RETURN:
                score = 0
                load_level(1)
                level_game = 1
                game_state = "playing"

            elif game_state == "final_victory" and event.key == pygame.K_RETURN:
                game_state = "start"

            elif game_state == "victory" and event.key == pygame.K_RETURN:
                level_game += 1
                if level_game > 3:
                    game_state = "final_victory"
                elif pygame.K_RETURN:
                    load_level(level_game)
                    game_state = "playing"

            elif game_state == "playing" and event.key == pygame.K_RETURN:
                bullets.append(Bullet(player.rect.right, player.rect.centery, player.facing_right))
                shot_sound.play()

    keys = pygame.key.get_pressed()

    # -------- GAME LOGIC --------
    if game_state == "playing":

        player.move(keys)

        # Camera
        offset_x = player.rect.x - WIDTH // 2
        offset_x = max(0, min(LEVEL_WIDTH - WIDTH, offset_x))

        # מעבר שלב
        if player.rect.colliderect(gate.rect):
            game_state = "victory"


        # Candies
        spawn_timer += 1
        if spawn_timer > 200:
            candies.append(Candy())
            spawn_timer = 0

        for c in candies:
            c.move()

        # Bacteria
        for b in bacteria:
            b.move(player.rect)

        # Bullets
        for bullet in bullets[:]:
            bullet.move()
            if bullet.out_of_range():
                bullets.remove(bullet)

        # Bullet hits
        for bullet in bullets[:]:
            for b in bacteria[:]:
                if bullet.rect.colliderect(b.rect):
                    bullets.remove(bullet)
                    bacteria.remove(b)
                    score += 50
                    break

        # Player damage
        for b in bacteria[:]:
            if player.rect.colliderect(b.rect):
                player.hp -= b.damage
                bacteria.remove(b)
                player_hit_sound.play()

            if hasattr(b, 'projectiles'):
                for proj in b.projectiles[:]:
                    if player.rect.colliderect(proj.rect):
                        player.hp -= proj.damage
                        b.projectiles.remove(proj)

        for s in candies[:]:
            if player.rect.colliderect(s.rect):
                player.hp -= 5
                candies.remove(s)

        # Cola pits
        for c in cola_pits:
            if player.rect.colliderect(c):
                if current_time - last_damage_time > damage_delay:
                    player.hp -= 2
                    last_damage_time = current_time

        # Platforms
        for p in platforms:
            if player.rect.colliderect(p):
                player.rect.bottom = p.rect.top
                player.vel_y = 0
                player.on_ground = True

        # Death
        if player.hp <= 0:
            save_score(score)
            game_over_sound.play()
            game_state = "game_over"

    # -------- DRAW --------
    if game_state == "start":
        start_screen.draw(screen)

    elif game_state == "playing":
        screen.fill(GUM_PINK)

        for x in range(0, LEVEL_WIDTH, floor_img.get_width()):
            screen.blit(floor_img, (x - offset_x, 330))

        for c in cola_pits:
            c.draw(offset_x)

        player.draw(offset_x)

        for b in bacteria:
            b.draw(offset_x)

        for s in candies:
            s.draw(offset_x)

        for p in platforms:
            p.draw(offset_x)

        for bullet in bullets:
            bullet.draw(offset_x)

        gate.draw(offset_x)

        hp_text = font.render(f"HP: {player.hp}", True, BLUE)
        score_text = font.render(f"Score: {score}", True, WHITE)
        level_game_text = font.render(f"level: {level_game}", True, YELLOW)

        screen.blit(hp_text, (20, 20))
        screen.blit(score_text, (20, 60))
        screen.blit(level_game_text,(350,20))
    elif game_state == "game_over":
        game_over_screen.draw(screen, score)

    elif game_state == "victory":
        victory_screen.draw(screen, score)

    elif game_state == "final_victory":
        final_victory_screen.draw(screen, score)

    pygame.display.update()
