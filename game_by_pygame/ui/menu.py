import pygame
from game_tooth_vs_bacteria.game_by_pygame.settings import WHITE, GREEN, TITLE, SCREEN_WIDTH, SCREEN_HEIGHT

class MainMenu:
    def __init__(self):
        self.title_font = pygame.font.SysFont("Arial", 64, bold=True)
        self.prompt_font = pygame.font.SysFont("Arial", 32)

    def draw(self, surface):
        """מצייר את התפריט למסך"""
        # כותרת המשחק
        title_surf = self.title_font.render(TITLE, True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        surface.blit(title_surf, title_rect)

        # כפתור/טקסט התחלה
        prompt_surf = self.prompt_font.render("Press ENTER to Start", True, GREEN)
        prompt_rect = prompt_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        surface.blit(prompt_surf, prompt_rect)