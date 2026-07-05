import pygame
import sys


class PlayerCore:
    def __init__(self, width=1000, height=600):
        self.width = width
        self.height = height
        
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.LIGHT_GRAY = (200, 200, 200)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.SEMI_TRANSPARENT_BLACK = (0, 0, 0, 100)
        
        try:
            self.font = pygame.font.SysFont(["Microsoft YaHei", "SimHei", "Arial"], 32)
            self.text_font = pygame.font.SysFont(["Microsoft YaHei", "SimHei", "Arial"], 28)
            self.small_font = pygame.font.SysFont(["Microsoft YaHei", "SimHei", "Arial"], 20)
            self.button_font = pygame.font.SysFont(["Microsoft YaHei", "SimHei", "Arial"], 16)
        except Exception:
            self.font = pygame.font.Font(None, 32)
            self.text_font = pygame.font.Font(None, 28)
            self.small_font = pygame.font.Font(None, 20)
            self.button_font = pygame.font.Font(None, 16)
        
        self.current_mode = "normal"
        self.is_auto_play = False
        self.is_skip_mode = False
        self.is_recall_mode = False
        self.is_playing = False
        self.current_segment_index = 0
        self.timeline = []
        self.metadata = {}
        
        self.recall_scroll = 0
        self.recall_page_height = 500
        
        self.volume_level = 2
        self.volume_steps = [0.0, 0.25, 0.5, 0.75, 1.0]
        pygame.mixer.music.set_volume(self.volume_steps[self.volume_level])
        
        self.auto_speed_level = 1
        self.auto_speed_factors = [0.5, 1.0, 2.0]
        self.auto_timer = 0
        self.segment_duration = 3.0
        
        self.skip_timer = 0
        self.skip_interval = 0.8
        
        self.first_music_completed = False
        
        self.message_timer = 0
        self.current_message = ""
        
        self.current_image_key = None
        self.previous_image_key = None
        self.current_image_index = -1
        self.transition_alpha = 0
        self.transition_duration = 60
        self.transition_timer = 0
        self.is_transitioning = False
        
        self.text_fade_alpha = 0
        self.text_fade_out_duration = 60
        self.text_fade_in_duration = 60
        self.text_fade_delay = 60
        self.text_fade_timer = 0
        self.is_text_fading = False
        self.is_text_fade_out = True
        self.should_show_text = True
        self.image_switched = False
    
    def set_timeline(self, timeline):
        self.timeline = timeline
    
    def set_metadata(self, metadata):
        self.metadata = metadata
    
    def get_current_segment(self):
        if self.timeline and self.current_segment_index < len(self.timeline):
            return self.timeline[self.current_segment_index]
        return None
    
    def draw_text_segment(self, screen, segment):
        if segment and self.should_show_text and not (self.is_text_fading and self.text_fade_alpha >= 255):
            text = segment["text"]
            lines = text.split('，')
            lines = lines[:5]
            
            text_bg_surface = pygame.Surface((850, 280), pygame.SRCALPHA)
            pygame.draw.rect(text_bg_surface, self.SEMI_TRANSPARENT_BLACK, (0, 0, 850, 280), border_radius=10)
            screen.blit(text_bg_surface, (75, self.height - 380))
            
            y = self.height - 160
            for line in reversed(lines):
                if line != lines[-1]:
                    line += '，'
                
                text_surface_shadow = self.text_font.render(line, True, (0, 0, 0))
                for offset in [(-1, -1), (-1, 1), (1, -1), (1, 1), (2, 2), (-2, -2), (2, -2), (-2, 2)]:
                    text_rect_shadow = text_surface_shadow.get_rect(center=(self.width/2 + offset[0], y + offset[1]))
                    screen.blit(text_surface_shadow, text_rect_shadow)
                
                text_surface = self.text_font.render(line, True, self.WHITE)
                text_rect = text_surface.get_rect(center=(self.width/2, y))
                screen.blit(text_surface, text_rect)
                y -= 50
    
    def adjust_volume(self, delta):
        new_level = max(0, min(4, self.volume_level + delta))
        if new_level != self.volume_level:
            self.volume_level = new_level
            pygame.mixer.music.set_volume(self.volume_steps[self.volume_level])
    
    def toggle_play_pause(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
        else:
            pygame.mixer.music.unpause()
            self.is_playing = True
    
    def toggle_auto_play(self):
        self.is_auto_play = not self.is_auto_play
        if self.is_auto_play:
            self.auto_timer = 0
            self.is_playing = True
    
    def toggle_skip_mode(self):
        self.is_skip_mode = not self.is_skip_mode
        if self.is_skip_mode:
            self.skip_timer = 0
    
    def toggle_recall_mode(self):
        self.is_recall_mode = not self.is_recall_mode
        if self.is_recall_mode:
            self.recall_scroll = 0
    
    def adjust_recall_scroll(self, delta):
        self.recall_scroll += delta
        max_scroll = self.get_recall_content_height() - self.recall_page_height
        if max_scroll > 0:
            self.recall_scroll = max(0, min(max_scroll, self.recall_scroll))
        else:
            self.recall_scroll = 0
    
    def get_recall_content_height(self):
        if not self.timeline:
            return 0
        line_height = 40
        base_padding = 100
        return base_padding + len(self.timeline) * line_height
    
    def draw_recall_mode(self, screen):
        screen.fill(self.BLACK)
        
        title = f"回想 - {self.metadata.get('title', '')}"
        title_surface = self.font.render(title, True, self.WHITE)
        screen.blit(title_surface, (self.width/2 - title_surface.get_width()/2, 30))
        
        hint_surface = self.small_font.render("(↑/↓滚动, ESC或R退出回想)", True, self.GRAY)
        screen.blit(hint_surface, (self.width/2 - hint_surface.get_width()/2, 60))
        
        if not self.timeline:
            no_text = self.text_font.render("暂无文本内容", True, self.GRAY)
            screen.blit(no_text, (self.width/2 - no_text.get_width()/2, self.height/2))
            pygame.display.flip()
            return
        
        line_height = 40
        start_y = 100 - self.recall_scroll
        
        current_seg = self.current_segment_index
        
        for i, segment in enumerate(self.timeline):
            text = segment.get("text", "")
            if not text:
                continue
            
            y = start_y + i * line_height
            
            if y < -50 or y > self.height:
                continue
            
            is_current = (i == current_seg)
            text_color = self.YELLOW if is_current else self.WHITE
            
            text_surface = self.text_font.render(text, True, text_color)
            
            if is_current and 0 <= y - 25 and y + 10 < self.height - 100:
                bg_rect = pygame.Rect(20, y - 25, self.width - 40, 35)
                if bg_rect.width > 0 and bg_rect.height > 0:
                    pygame.draw.rect(screen, self.GREEN, bg_rect, border_radius=5)
                    text_surface = self.text_font.render(text, True, self.BLACK)
            
            screen.blit(text_surface, (40, y - 25))
        
        total_height = self.get_recall_content_height()
        if total_height > self.recall_page_height:
            scrollbar_height = int(self.recall_page_height * self.recall_page_height / total_height)
            scrollbar_y = 100 + int(self.recall_scroll * (self.recall_page_height - scrollbar_height) / (total_height - self.recall_page_height))
            pygame.draw.rect(screen, self.GRAY, (self.width - 20, scrollbar_y, 10, scrollbar_height))
        
        pygame.display.flip()
    
    def adjust_auto_speed(self, delta):
        new_level = max(0, min(2, self.auto_speed_level + delta))
        if new_level != self.auto_speed_level:
            self.auto_speed_level = new_level
    
    def go_to_start(self):
        self.current_segment_index = 0
    
    def next_segment(self):
        if self.timeline and self.current_segment_index < len(self.timeline) - 1:
            self.current_segment_index += 1
            self.is_playing = True
    
    def show_message(self, message):
        self.current_message = message
        self.message_timer = 120
    
    def get_current_background_image_key(self):
        if self.current_segment_index < 4:
            return "lantern"
        else:
            return "rain_street"
    
    def check_image_transition(self, load_image_callback):
        current_segment = self.get_current_segment()
        if current_segment and "background" in current_segment:
            new_image_key = current_segment["background"]
            if self.current_image_index != self.current_segment_index:
                if self.current_segment_index == 4 and not self.image_switched:
                    if not self.is_transitioning and not self.is_text_fading:
                        self.previous_image_key = self.current_image_key
                        self.current_image_key = new_image_key
                        self.current_image_index = self.current_segment_index
                        self.is_transitioning = True
                        self.transition_timer = 0
                        self.transition_alpha = 0
                        self.is_text_fading = True
                        self.text_fade_timer = 0
                        self.text_fade_alpha = 0
                        self.is_text_fade_out = True
                        self.should_show_text = False
                        return new_image_key
        return None
    
    def update(self, load_image_callback):
        if self.is_auto_play and self.is_playing:
            if self.timeline and self.current_segment_index < len(self.timeline):
                self.auto_timer += 1 / 60.0
                segment = self.timeline[self.current_segment_index]
                duration = segment.get("duration", self.segment_duration)
                effective_duration = duration / self.auto_speed_factors[self.auto_speed_level]
                
                if self.auto_timer >= effective_duration:
                    if self.current_segment_index < len(self.timeline) - 1:
                        self.current_segment_index += 1
                        segment = self.timeline[self.current_segment_index]
                        if "image" in segment:
                            load_image_callback(segment["image"])
                    self.auto_timer = 0
        
        if self.is_skip_mode:
            if self.timeline and self.current_segment_index < len(self.timeline) - 1:
                self.skip_timer += 1 / 60.0
                if self.skip_timer >= self.skip_interval:
                    self.current_segment_index += 1
                    segment = self.timeline[self.current_segment_index]
                    if "image" in segment:
                        load_image_callback(segment["image"])
                    self.skip_timer = 0
        
        if not self.first_music_completed:
            if not pygame.mixer.music.get_busy():
                self.first_music_completed = True
        
        if self.message_timer > 0:
            self.message_timer -= 1
        
        if self.is_transitioning:
            self.transition_timer += 1
            progress = min(1.0, self.transition_timer / self.transition_duration)
            self.transition_alpha = int(255 * progress)
            
            if self.transition_timer >= self.transition_duration:
                self.is_transitioning = False
                self.previous_image_key = None
                self.transition_alpha = 0
                self.image_switched = True
        
        if self.is_text_fading:
            self.text_fade_timer += 1
            
            if self.is_text_fade_out:
                progress = min(1.0, self.text_fade_timer / self.text_fade_out_duration)
                self.text_fade_alpha = int(255 * progress)
                
                if self.text_fade_timer >= self.text_fade_out_duration:
                    self.is_text_fade_out = False
                    self.text_fade_timer = 0
                    self.text_fade_alpha = 255
                    self.should_show_text = True
            else:
                if self.text_fade_timer < self.text_fade_delay:
                    self.text_fade_alpha = 255
                else:
                    fade_in_timer = self.text_fade_timer - self.text_fade_delay
                    progress = min(1.0, fade_in_timer / self.text_fade_in_duration)
                    self.text_fade_alpha = int(255 * (1 - progress))
                    
                    if fade_in_timer >= self.text_fade_in_duration:
                        self.is_text_fading = False
                        self.text_fade_alpha = 0
        
        expected_image_key = self.get_current_background_image_key()
        if expected_image_key != self.current_image_key and not self.is_transitioning and not self.is_text_fading:
            self.current_image_key = expected_image_key
            if load_image_callback:
                load_image_callback(expected_image_key)
    
    def draw(self, screen, current_image_surface, previous_image_surface=None):
        screen.fill(self.BLACK)
        
        if previous_image_surface and self.is_transitioning:
            screen.blit(previous_image_surface, (0, 0))
            
            fade_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            fade_surface.fill((0, 0, 0, self.transition_alpha))
            screen.blit(fade_surface, (0, 0))
        elif current_image_surface:
            screen.blit(current_image_surface, (0, 0))
            
            if self.is_text_fading and not self.is_text_fade_out and self.text_fade_timer >= self.text_fade_delay:
                fade_in_timer = self.text_fade_timer - self.text_fade_delay
                progress = min(1.0, fade_in_timer / self.text_fade_in_duration)
                dim_alpha = int(80 * progress)
                
                dim_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                dim_surface.fill((0, 0, 0, dim_alpha))
                screen.blit(dim_surface, (0, 0))
            elif not self.is_text_fading:
                dim_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                dim_surface.fill((0, 0, 0, 80))
                screen.blit(dim_surface, (0, 0))
        
        title = self.metadata.get("title", "")
        author = self.metadata.get("author", "")
        
        title_surface = self.font.render(title, True, self.WHITE)
        author_surface = self.font.render(f"作者: {author}", True, self.WHITE)
        
        screen.blit(title_surface, (self.width/2 - title_surface.get_width()/2, 50))
        screen.blit(author_surface, (self.width/2 - author_surface.get_width()/2, 80))
        
        current_segment = self.get_current_segment()
        self.draw_text_segment(screen, current_segment)
        
        progress_text = f"页码: {self.current_segment_index + 1}/{len(self.timeline)}"
        progress_surface = self.small_font.render(progress_text, True, self.YELLOW)
        screen.blit(progress_surface, (self.width - 150, 10))
        
        mode_text = "自动" if self.is_auto_play else "手动"
        mode_color = self.GREEN if self.is_auto_play else self.YELLOW
        mode_surface = self.small_font.render(f"模式: {mode_text}", True, mode_color)
        screen.blit(mode_surface, (10, 10))
        
        skip_text = "跳过: 开" if self.is_skip_mode else "跳过: 关"
        skip_color = self.GREEN if self.is_skip_mode else self.WHITE
        skip_surface = self.small_font.render(skip_text, True, skip_color)
        screen.blit(skip_surface, (10, 35))
        
        speed_names = ["慢速", "正常", "快速"]
        speed_text = f"速度: {speed_names[self.auto_speed_level]}"
        speed_surface = self.small_font.render(speed_text, True, self.WHITE)
        screen.blit(speed_surface, (10, 60))
        
        volume_text = f"音量: {self.volume_level * 25}%"
        volume_surface = self.small_font.render(volume_text, True, self.WHITE)
        screen.blit(volume_surface, (self.width - 260, 10))
        
        if self.message_timer > 0:
            message_surface = self.font.render(self.current_message, True, self.GREEN)
            message_rect = message_surface.get_rect(center=(self.width/2, self.height/2))
            
            bg_rect = message_rect.inflate(40, 20)
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_surface.fill((0, 0, 0, 200))
            screen.blit(bg_surface, bg_rect)
            pygame.draw.rect(screen, self.GREEN, bg_rect, 2, border_radius=5)
            
            screen.blit(message_surface, message_rect)
