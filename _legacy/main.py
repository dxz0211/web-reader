import os
import sys
from pathlib import Path
import pygame

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

pygame.init()

from player.player import ImmersionPlayer
from editor.editor import ImmersionEditor


class Launcher:
    def __init__(self):
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("沉浸式阅读平台")
        
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.LIGHT_GRAY = (200, 200, 200)
        self.DARK_GRAY = (64, 64, 64)
        self.BLUE = (0, 100, 200)
        self.LIGHT_BLUE = (0, 150, 255)
        self.GREEN = (0, 150, 0)
        self.LIGHT_GREEN = (0, 200, 0)
        self.YELLOW = (255, 255, 0)
        
        try:
            self.title_font = pygame.font.SysFont(["Microsoft YaHei", "SimHei", "Arial"], 48)
            self.button_font = pygame.font.SysFont(["Microsoft YaHei", "SimHei", "Arial"], 28)
            self.subtitle_font = pygame.font.SysFont(["Microsoft YaHei", "SimHei", "Arial"], 20)
        except Exception:
            self.title_font = pygame.font.Font(None, 48)
            self.button_font = pygame.font.Font(None, 28)
            self.subtitle_font = pygame.font.Font(None, 20)
        
        self.editor_button = pygame.Rect(200, 250, 400, 80)
        self.player_button = pygame.Rect(200, 380, 400, 80)
        
        self.running = True
    
    def draw(self):
        self.screen.fill(self.DARK_GRAY)
        
        title_text = self.title_font.render("沉浸式阅读平台", True, self.WHITE)
        title_rect = title_text.get_rect(center=(self.width // 2, 120))
        self.screen.blit(title_text, title_rect)
        
        subtitle_text = self.subtitle_font.render("请选择要启动的模块", True, self.LIGHT_GRAY)
        subtitle_rect = subtitle_text.get_rect(center=(self.width // 2, 180))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        pygame.draw.rect(self.screen, self.BLUE, self.editor_button, border_radius=10)
        pygame.draw.rect(self.screen, self.LIGHT_BLUE, self.editor_button, 3, border_radius=10)
        editor_text = self.button_font.render("编辑器", True, self.WHITE)
        editor_rect = editor_text.get_rect(center=self.editor_button.center)
        self.screen.blit(editor_text, editor_rect)
        
        pygame.draw.rect(self.screen, self.GREEN, self.player_button, border_radius=10)
        pygame.draw.rect(self.screen, self.LIGHT_GREEN, self.player_button, 3, border_radius=10)
        player_text = self.button_font.render("播放器", True, self.WHITE)
        player_rect = player_text.get_rect(center=self.player_button.center)
        self.screen.blit(player_text, player_rect)
        
        hint_text = self.subtitle_font.render("点击按钮启动对应模块，ESC退出", True, self.GRAY)
        hint_rect = hint_text.get_rect(center=(self.width // 2, 520))
        self.screen.blit(hint_text, hint_rect)
        
        pygame.display.flip()
    
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            return "exit"
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
                return "exit"
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                
                if self.editor_button.collidepoint(mouse_x, mouse_y):
                    return "editor"
                
                if self.player_button.collidepoint(mouse_x, mouse_y):
                    return "player"
        
        return None
    
    def run(self):
        clock = pygame.time.Clock()
        
        while self.running:
            for event in pygame.event.get():
                result = self.handle_event(event)
                if result:
                    return result
            
            self.draw()
            clock.tick(60)
        
        return "exit"


if __name__ == "__main__":
    launcher = Launcher()
    choice = launcher.run()
    
    if choice == "editor":
        editor = ImmersionEditor()
        editor.run()
    elif choice == "player":
        player = ImmersionPlayer()
        player.run()
    
    pygame.quit()
    sys.exit()
