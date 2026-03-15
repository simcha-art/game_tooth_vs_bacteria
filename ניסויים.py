import pygame
import random
import json
import sys

from bacterias import *
from tooth import *
from bullets import *
from settings import *
from pro_main import *
from obstacles import *
from screens import *
from data import *

pygame.init()

# ---------------- MAIN GAME ----------------

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f and game_state == "playing":
                bullets.append(Bullet(player.rect.right, player.rect.centery,direction=True))

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

        # --- שינוי 1: חיידקים וקליעים ---
        for b in bacteria:
            b.move(player.rect)  # עכשיו החיידקים מקבלים את מיקום השן כדי לעקוב/לירות!
        for bullet in bullets:
            bullet.move()
        # ----------------------------------

        # פגיעות קליעים בחיידקים
        for bullet in bullets[:]:
            for b in bacteria[:]:
                if bullet.rect.colliderect(b.rect):
                    bullets.remove(bullet)
                    bacteria.remove(b)
                    score += 50
                    break

        # --- שינוי 2 ו-3: פגיעות השחקן מחיידקים וקליעי חומצה ---
        for b in bacteria[:]:
            # בדיקת התנגשות עם גוף החיידק עצמו
            if player.rect.colliderect(b.rect):
                player.hp -= b.damage  # שימוש בנזק הדינמי של המחלקה (10, 20 או 5)
                bacteria.remove(b)

            # בדיקת התנגשות עם קליעי החומצה (אם זה חיידק יורה)
            if hasattr(b, 'projectiles'):  # בודק אם לחיידק הזה יש בכלל רשימת קליעים
                for proj in b.projectiles[:]:
                    if player.rect.colliderect(proj.rect):
                        player.hp -= proj.damage  # מוריד חיים לפי נזק החומצה
                        b.projectiles.remove(proj)  # מעלים את טיפת החומצה שפגעה
        # --------------------------------------------------------

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

        # פונקציית הציור של החיידקים מציירת גם את קליעי החומצה אוטומטית (אם יש להם)
        for b in bacteria: b.draw(offset_x)

        for s in candies: s.draw(offset_x)
        for bullet in bullets: bullet.draw(offset_x)

        hp_text = font.render(f"HP: {player.hp}", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(hp_text, (20, 20))
        screen.blit(score_text, (20, 60))

    pygame.display.update()