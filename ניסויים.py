from bacterias import *
from settings import *


# ---------------- פונקציית איפוס שלב ----------------
# מאפסת את נתוני השחקן, מנקה רשימות ומייצרת חיידקים חדשים
def reset_level(player, bacteria, bullets, candies):
    player.hp = 100
    player.rect.topleft = (100, 400)
    bullets.clear()
    candies.clear()
    # עדכון רשימת החיידקים בזיכרון (Slice Assignment)
    bacteria[:] = [Bacteria(random.randint(300, 4000), 460) for b in range(10)]


# ---------------- מסך פתיחה ----------------
# מציג את תמונת הגיבור וכותרת המשחק לפני תחילת המשחק
class StartScreen:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 55, bold=True)
        # ניסיון טעינת תמונת השן המסתכלת שמאלה (300x300)
        self.image = pygame.transform.scale(large_tooth_left, (400, 400))

    def draw(self, surface):
        surface.fill(PINK)
        if self.image:
            # מירכוס התמונה בחלק העליון של המסך
            img_rect = self.image.get_rect(center=(WIDTH // 2 - 20, HEIGHT // 3 + 60))
            surface.blit(self.image, img_rect)

        # כותרת המשחק - ממוקמת מתחת לתמונה
        title_surf = self.font.render("Tooth vs Bacteria: The Adventure", True, RED)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, 90))
        surface.blit(title_surf, title_rect)

        # הוראת התחלה לשחקן
        prompt_surf = self.font.render("Press ENTER to Start", True, BLUE)
        prompt_rect = prompt_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 140))
        surface.blit(prompt_surf, prompt_rect)


# ---------------- מסך הפסד ----------------
# מוצג כשהחיים נגמרים, כולל הניקוד הסופי ואפשרות לניסיון חוזר
class GameOverScreen:
    def __init__(self):
        self.title_font = pygame.font.SysFont("Arial", 80, bold=True)
        self.info_font = pygame.font.SysFont("Arial", 40, bold=True)
        # טעינת תמונת השן שמאלה (קצת קטנה יותר למסך זה - 150x150)
        try:
            self.image = large_tooth_left
            self.image = pygame.transform.scale(self.image, (150, 150))
        except:
            self.image = None

    def draw(self, surface, final_score):
        surface.fill((150, 0, 0))  # רקע אדום כהה להדגשת ההפסד

        if self.image:
            # ציור התמונה בחלק העליון מעל הכותרת
            img_rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 4 - 50))
            surface.blit(self.image, img_rect)

        # כיתוב Game Over גדול
        title_surf = self.title_font.render("GAME OVER", True, WHITE)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 20))
        surface.blit(title_surf, title_rect)

        # הצגת הניקוד שהושג
        score_surf = self.info_font.render(f"Final Score: {final_score}", True, YELLOW)
        score_rect = score_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        surface.blit(score_surf, score_rect)

        # הוראת חזרה למשחק
        restart_surf = self.info_font.render("Press ENTER to play again", True, GREEN)
        restart_rect = restart_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))
        surface.blit(restart_surf, restart_rect)


# ---------------- מסך ניצחון ----------------
# מוצג לאחר סיום השלב, מאפשר בחירה בין משחק חוזר או מעבר לשלב הבא
class VictoryScreen:
    def __init__(self):
        self.title_font = pygame.font.SysFont("Arial", 64, bold=True)
        self.info_font = pygame.font.SysFont("Arial", 42)
        # טעינת תמונת השן שמאלה (150x150)
        try:
            self.image = large_tooth_left
            self.image = pygame.transform.scale(self.image, (150, 150))
        except:
            self.image = None

    def draw(self, surface, final_score):
        # שימוש ברקע תכלת כדי שהטקסט הצהוב יהיה קריא
        surface.fill(GREEN)

        if self.image:
            # ציור התמונה בחלק העליון מעל הכותרת
            img_rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 4 - 50))
            surface.blit(self.image, img_rect)

        title_surf = self.title_font.render("VICTORY!", True, PURPLE)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 20))
        surface.blit(title_surf, title_rect)

        score_surf = self.info_font.render(f"You saved the teeth! Score: {final_score}", True, BLUE)
        score_rect = score_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        surface.blit(score_surf, score_rect)



        # מעבר לשלב הבא (בצבע צהוב בולט)
        next_surf = self.info_font.render("Press SPACE for Level II", True, PURPLE)
        next_rect = next_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))
        surface.blit(next_surf, next_rect)
# ---------------- מסך הניצחון הסופי ----------------
# מוצג לאחר ניצחון בשלב 2 - סיום המשחק
import random

# ---------------- מחלקת בלון ----------------
import random


# ---------------- מחלקת בלון צבעוני ----------------

# מנהלת בלון שנע במהירות קבועה ללא חוטים מצוירים
class Balloon:
    def __init__(self, balloon_images, initial_y):
        self.balloon_images = balloon_images
        # הגדרת מהירות קבועה ומהירה (במקום רנדומלית)
        self.speed = 10
        self.reset(initial_y)

    def reset(self, new_y=None):
        # בחירת תמונה אקראית מתוך ה-5
        random_base_image = random.choice(self.balloon_images)

        # פריסה על כל רוחב המסך
        self.x = random.randint(-100, WIDTH-400)

        # אם קיבלנו מיקום Y ספציפי (ביצירה הראשונית), נשתמש בו.
        # אחרת, נשים את הבלון בדיוק מתחת למסך כדי לשמור על הקצב.
        if new_y is not None:
            self.y = new_y
        else:
            self.y = HEIGHT + 50

            # שינוי גודל אקראי קל לגיוון ויזואלי
        scale_factor = random.uniform(0.6, 0.8)
        self.image = pygame.transform.scale(random_base_image,
                                            (int(random_base_image.get_width() * scale_factor),
                                             int(random_base_image.get_height() * scale_factor)))

    def update(self):
        self.y -= self.speed  # מהירות קבועה
        # כשהבלון יוצא מהמסך, הוא חוזר לסוף הטור
        if self.y < -self.image.get_height() - 20:
            self.reset()

    def draw(self, surface):
        # ציור התמונה בלבד (החוט כבר חלק מהתמונה שלך)
        surface.blit(self.image, (self.x, self.y))# ---------------- מסך הניצחון הסופי המעודכן ----------------
# ---------------- מסך הניצחון הסופי עם בלונים צבעוניים ----------------
class FinalVictoryScreen:
    def __init__(self):
        self.title_font = pygame.font.SysFont("Arial", 75, bold=True)
        self.info_font = pygame.font.SysFont("Arial", 55, bold=True)

        self.balloon_images = [
            YELLO_BALLOON_IMG, RED_BALLOON_IMG, PURPLE_BALLOON_IMG,
            GREEN_BALLOON_IMG, LIGHT_BLUE_BALLOON_IMG
        ]

        # יצירת 15 בלונים במרווחים קבועים כדי למנוע "גלים"
        self.balloons = []
        num_balloons = 18
        # המרווח האנכי בין בלון לבלון (מחושב לפי גובה המסך כדי שיהיה רצף)
        spacing = (HEIGHT + 400) / num_balloons

        for i in range(num_balloons):
            # כל בלון מקבל גובה התחלתי שונה בטור
            start_y = HEIGHT + (i * spacing)
            self.balloons.append(Balloon(self.balloon_images, start_y))

        try:
            self.image = pygame.transform.scale(large_tooth_left, (400, 400))
        except:
            self.image = None

    def draw(self, surface, final_score):
        surface.fill(YELLOW)

        # הבלונים עכשיו יזרמו בקצב של מכונה
        for b in self.balloons:
            b.update()
            b.draw(surface)

        if self.image:
            img_rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 40))
            surface.blit(self.image, img_rect)

        # טקסטים
        win_surf = self.title_font.render("YOU WON! HOORAY!", True, GREEN)
        surface.blit(win_surf, win_surf.get_rect(center=(WIDTH // 2, 80)))

        saved_surf = self.info_font.render("The Tooth is Safe Forever!", True, PURPLE)
        surface.blit(saved_surf, saved_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 110)))

        score_surf = self.info_font.render(f"Total Score: {final_score}", True, RED)
        surface.blit(score_surf, score_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 170)))

        prompt_surf = pygame.font.SysFont("Arial", 25).render("Press ENTER for Main Menu", True, BLUE)
        surface.blit(prompt_surf, prompt_surf.get_rect(center=(WIDTH // 2, HEIGHT - 70)))
def test_loop():
    start = StartScreen()
    game_over = GameOverScreen()
    victory = VictoryScreen()
    final_win = FinalVictoryScreen() # יצירת המסך החדש

    current_view = "START"
    test_score = 300

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: current_view = "START"
                if event.key == pygame.K_2: current_view = "FAIL"
                if event.key == pygame.K_3: current_view = "WIN"
                if event.key == pygame.K_4: current_view = "FINAL" # מקש חדש לבדיקה

        # ציור המסך הנבחר
        if current_view == "START":
            start.draw(screen)
        elif current_view == "FAIL":
            game_over.draw(screen, test_score)
        elif current_view == "WIN":
            victory.draw(screen, test_score)
        elif current_view == "FINAL":
            final_win.draw(screen, test_score)

        # טקסט עזרה קטן בתחתית
        help_font = pygame.font.SysFont("Arial", 16)
        help_surf = help_font.render("Keys: 1-Start, 2-Fail, 3-Win Lvl1, 4-Final Win", True, BLACK if current_view == "FINAL" else WHITE)
        screen.blit(help_surf, (10, HEIGHT - 25))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    test_loop()