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

        #ניהול קולה
        # 1. הגדרת המכשול (בור הקולה)
        # 350 זה המיקום, 490 זה הגובה (טיפה מעל הרצפה כדי שיזהה מגע)
        cola_pit = pygame.Rect(350, 490, 120, 110)

        # 2. בדיקת מגע והורדת ניקוד (בדיוק כמו בחיידקים)
        # 1. הגדרת המכשול
        cola_pit = pygame.Rect(350, 490, 120, 110)

        if player.rect.colliderect(cola_pit):
            if can_lose_score:  # המנעול שלנו
                player.hp -= 10  # מוריד 10 מהחיים (HP)
                can_lose_score = False  # נועל כדי שלא ירד עוד
                print(f"Hit Cola! HP left: {player.hp}")

            player.speed = 1  # האטה בזמן השהייה
        else:
            can_lose_score = True  # משחרר את הנעילה רק כשיוצאים מהבור
            player.speed = 5
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



        if player.hp <= 0:
            save_score(score)
            game_over_sound.play()
            reset_level(player, bacteria, bullets, candies)
            score = 0

        # ציור המסך
        screen.fill((GUM_PINK))
        #pygame.draw.rect(screen, BROWN, (0 - offset_x, 485, LEVEL_WIDTH, 100))# רצפת המשחק
        for x in range(0, LEVEL_WIDTH, floor_img.get_width()):
            screen.blit(floor_img, (x - offset_x, 330))
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