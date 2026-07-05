import pygame
import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class EditorCore:
    def __init__(self, width=1200, height=800):
        self.width = width
        self.height = height
        
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.LIGHT_GRAY = (200, 200, 200)
        self.DARK_GRAY = (64, 64, 64)
        self.BLUE = (0, 100, 200)
        self.LIGHT_BLUE = (0, 150, 255)
        self.GREEN = (0, 150, 0)
        self.LIGHT_GREEN = (0, 200, 0)
        self.RED = (150, 0, 0)
        self.LIGHT_RED = (200, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.SEMI_TRANSPARENT_BLACK = (0, 0, 0, 180)
        self.SEMI_TRANSPARENT_WHITE = (255, 255, 255, 200)
        
        try:
            self.font = pygame.font.SysFont(["Microsoft YaHei", "SimHei", "Arial"], 18)
            self.title_font = pygame.font.SysFont(["Microsoft YaHei", "SimHei", "Arial"], 20)
            self.small_font = pygame.font.SysFont(["Microsoft YaHei", "SimHei", "Arial"], 14)
        except Exception:
            self.font = pygame.font.Font(None, 18)
            self.title_font = pygame.font.Font(None, 20)
            self.small_font = pygame.font.Font(None, 14)
        
        self.current_mode = "normal"
        self.current_file_path = None
        self.is_modified = False
        
        self.text_segments = []
        self.selected_segment_index = -1
        self.is_editing_text = False
        self.editing_segment_index = -1
        self.editing_text = ""
        self.cursor_pos = 0
        
        self.images = []
        self.selected_image_index = -1
        self.audio_file = None
        self.audio_duration = 0
        
        self.timeline_tracks = {
            "text": [],
            "image": [],
            "audio": []
        }
        self.selected_track = "text"
        self.selected_node = {
            "track": None,
            "index": -1
        }
        self.is_dragging_node = False
        self.drag_start_time = 0
        self.drag_start_x = 0
        self.timeline_scale = 60
        self.timeline_offset = 0
        self.timeline_duration = 60
        self.track_height = 30
        
        self.message_timer = 0
        self.current_message = ""
        
        self.recent_files = []
        
        self.text_area_rect = pygame.Rect(20, 100, 500, 400)
        self.resource_area_rect = pygame.Rect(540, 100, 640, 400)
        self.timeline_area_rect = pygame.Rect(20, 520, 1160, 200)
        self.menu_bar_rect = pygame.Rect(0, 0, self.width, 40)
        self.toolbar_rect = pygame.Rect(0, 40, self.width, 50)
        self.status_bar_rect = pygame.Rect(0, self.height - 30, self.width, 30)
    
    def show_message(self, message):
        self.current_message = message
        self.message_timer = 180
    
    def update(self):
        if self.message_timer > 0:
            self.message_timer -= 1
    
    def get_window_title(self):
        if self.current_file_path:
            filename = os.path.basename(self.current_file_path)
            modified_str = " *" if self.is_modified else ""
            return f"沉浸式阅读编辑器 - {filename}{modified_str}"
        return "沉浸式阅读编辑器 - 未命名*"