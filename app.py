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








# ---------------- MAIN GAME ----------------

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

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
                player.hp -= 10
                bacteria.remove(b)
                player_hit_sound.play()

        for s in candies[:]:
            if player.rect.colliderect(s.rect):
                player.hp -= 5
                candies.remove(s)

        # בור קולה
        for c in cola_pits:
            if player.rect.colliderect(c):
                player.hp = 0

        if player.hp <= 0:
            save_score(score)
            game_over_sound.play()
            reset_level(player, bacteria, bullets, candies)
            score = 0

        # ציור המסך
        screen.fill((GUM_PINK))
        for x in range(0, LEVEL_WIDTH, floor_img.get_width()):
            screen.blit(floor_img, (x - offset_x, 330))
        for c in cola_pits: c.draw(offset_x)
        player.draw(offset_x)
        for b in bacteria: b.draw(offset_x)
        for s in candies: s.draw(offset_x)
        for p in platforms: p.draw(offset_x)
        for bullet in bullets: bullet.draw(offset_x)

        hp_text = font.render(f"HP: {player.hp}", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(hp_text, (20, 20))
        screen.blit(score_text, (20, 60))

    pygame.display.update()