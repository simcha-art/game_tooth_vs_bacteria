import pygame
from settings import *


class GameOverScreen:
    def __init__(self):
        self.title_font = pygame.font.SysFont("Arial", 64, bold=True)
        self.info_font = pygame.font.SysFont("Arial", 32)

    def draw(self, surface, final_score):
        title_surf = self.title_font.render("GAME OVER", True, RED)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        surface.blit(title_surf, title_rect)

        score_surf = self.info_font.render(f"Final Score: {final_score}", True, WHITE)
        score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        surface.blit(score_surf, score_rect)

        restart_surf = self.info_font.render("Press ENTER to return to Menu", True, GREEN)
        restart_rect = restart_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        surface.blit(restart_surf, restart_rect)


class VictoryScreen:
    def __init__(self):
        self.title_font = pygame.font.SysFont("Arial", 64, bold=True)
        self.info_font = pygame.font.SysFont("Arial", 32)

    def draw(self, surface, final_score):
        title_surf = self.title_font.render("VICTORY!", True, GREEN)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        surface.blit(title_surf, title_rect)

        score_surf = self.info_font.render(f"You saved the teeth! Score: {final_score}", True, WHITE)
        score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        surface.blit(score_surf, score_rect)

        restart_surf = self.info_font.render("Press ENTER to play again", True, YELLOW)
        restart_rect = restart_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        surface.blit(restart_surf, restart_rect)