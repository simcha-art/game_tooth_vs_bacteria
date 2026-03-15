import pygame
import random
import json
import sys

from bacterias import *
from tooth import *
from bullets import  *
from settings import *
from pro_main import *
from obstacles import *
from screens import *
from data import *


pygame.init()
pygame.mixer.init()

game_state = "start"

start_screen = StartScreen()
game_over_screen = GameOverScreen()
victory_screen = VictoryScreen()
final_victory_screen = FinalVictoryScreen()


#לבור קולה
last_damage_time = 0
damage_delay = 500



# ---------------- MAIN GAME ----------------

while True:
    clock.tick(60)
    current_time = pygame.time.get_ticks()

    if game_state == "start":
        start_screen.draw(screen)

    elif game_state == "game_over":
        game_over_screen.draw(screen, score)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if game_state == "start":
                if event.key == pygame.K_RETURN:
                    game_state = "playing"

            elif game_state == "game_over":
                if event.key == pygame.K_RETURN:
                    reset_level(player, bacteria, bullets, candies)
                    score = 0
                    game_state = "playing"

            elif game_state == "victory":
                if event.key == pygame.K_SPACE:
                    game_state = "playing"  # או level2

            elif game_state == "final_victory":
                if event.key == pygame.K_RETURN:
                    game_state = "start"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f and game_state == "playing":
                bullets.append(Bullet(player.rect.right, player.rect.centery,player.facing_right))
                shot_sound.play()

    keys = pygame.key.get_pressed()

    if game_state == "playing":
        # תנועה
        player.move(keys)

        # עדכון מצלמה
        offset_x = player.rect.x - WIDTH // 2
        offset_x = max(0, min(LEVEL_WIDTH - WIDTH, offset_x))

        if player.rect.colliderect(gate.rect):
            game_state = "victory"


        # ניהול סוכריות
        spawn_timer += 1
        if spawn_timer > 200:
            candies.append(Candy())
            spawn_timer = 0
        for c in candies:
            c.move()

        # חיידקים וקליעים
        for b in bacteria:
            b.move((player.rect))

        for bullet in bullets[:]:
            bullet.move()
            if bullet.out_of_range():
                bullets.remove(bullet)

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
                player.hp -= b.damage
                bacteria.remove(b)
                player_hit_sound.play()

            # בדיקת התנגשות עם קליעי החומצה (אם זה חיידק יורה)
            if hasattr(b, 'projectiles'):  # בודק אם לחיידק הזה יש בכלל רשימת קליעים
                for proj in b.projectiles[:]:
                    if player.rect.colliderect(proj.rect):
                        player.hp -= proj.damage  # מוריד חיים לפי נזק החומצה
                        b.projectiles.remove(proj)  # מעלים את טיפת החומצה שפגעה

        for s in candies[:]:
            if player.rect.colliderect(s.rect):
                player.hp -= 5
                candies.remove(s)

        #בור קולה
        for c in cola_pits:
            if player.rect.colliderect(c):
                if current_time -last_damage_time > damage_delay:
                    player.hp -= 2
                    last_damage_time = current_time

        #פלטפורמות
        for p in platforms:
            if player.rect.colliderect(p):
                player.rect.bottom = 350
                player.vel_y = 0
                player.on_ground = True

        if player.hp <= 0:
            save_score(score)
            game_over_sound.play()
            game_state = "game_over"
            reset_level(player, bacteria, bullets, candies)
            score = 0

        # ציור המסך


        elif game_state == "playing":
            screen.fill((GUM_PINK))
            # pygame.draw.rect(screen, BROWN, (0 - offset_x, 485, LEVEL_WIDTH, 100))# רצפת המשחק
            for x in range(0, LEVEL_WIDTH, floor_img.get_width()):
                screen.blit(floor_img, (x - offset_x, 330))

            for c in cola_pits: c.draw(offset_x)
            player.draw(offset_x)
            for b in bacteria: b.draw(offset_x)
            for s in candies: s.draw(offset_x)
            for p in platforms: p.draw(offset_x)
            for bullet in bullets: bullet.draw(offset_x)
            gate.draw(offset_x)

            hp_text = font.render(f"HP: {player.hp}", True, WHITE)
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(hp_text, (20, 20))
            screen.blit(score_text, (20, 60))

        elif game_state == "game_over":
            game_over_screen.draw(screen, score)

        elif game_state == "victory":
            victory_screen.draw(screen, score)

        elif game_state == "final_victory":
            final_victory_screen.draw(screen, score)


    pygame.display.update()