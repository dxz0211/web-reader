import pygame
import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

pygame.init()
pygame.mixer.init()

from player.data_loader import DataLoader
from player.ui_components import Button, ConfirmDialog
from player.save_load import SaveLoadManager
from player.media_handler import MediaHandler
from player.player_core import PlayerCore


class ImmersionPlayer:
    def __init__(self):
        self.width, self.height = 1000, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Immersion Reader Player")
        
        self.core = PlayerCore(self.width, self.height)
        self.save_load = SaveLoadManager()
        self.data_loader = DataLoader()
        self.media_handler = MediaHandler(self.data_loader)
        
        self.current_image_surface = None
        self.previous_image_surface = None
        
        self.confirm_dialog = None
        self.save_buttons = []
        self.load_buttons = []
        
        self.load_ims_file("data/sample.ims")
        
        if self.core.timeline:
            last_segment = self.core.timeline[-1]
            self.core.total_duration = last_segment["start_time"] + last_segment["duration"]
            
            self.current_image_surface = self.media_handler.load_image("lantern")
            
            self.media_handler.play_audio("rain_sound")
        
        self.init_buttons()
    
    def init_buttons(self):
        button_y = self.height - 60
        button_height = 40
        button_width = 85
        spacing = 20
        start_x = 20
        
        self.buttons = [
            Button(start_x, button_y, button_width, button_height, "播放", self.core.toggle_play_pause, (0, 100, 200), (0, 150, 255)),
            Button(start_x + (button_width + spacing) * 1, button_y, button_width, button_height, "自动", self.core.toggle_auto_play, (0, 150, 0), (0, 200, 0)),
            Button(start_x + (button_width + spacing) * 2, button_y, button_width, button_height, "跳过", self.core.toggle_skip_mode, (150, 100, 0), (200, 150, 0)),
            Button(start_x + (button_width + spacing) * 3, button_y, button_width, button_height, "存档", lambda: self.show_save_dialog(), (150, 0, 0), (200, 0, 0)),
            Button(start_x + (button_width + spacing) * 4, button_y, button_width, button_height, "读档", lambda: self.show_load_dialog(), (0, 0, 150), (0, 0, 200)),
            Button(start_x + (button_width + spacing) * 5, button_y, button_width, button_height, "回想", self.core.toggle_recall_mode, (100, 100, 0), (150, 150, 0)),
            Button(start_x + (button_width + spacing) * 6, button_y, button_width, button_height, "开头", self.go_to_start, (100, 100, 100), (150, 150, 150)),
        ]
        
        volume_x = self.width - 180
        self.volume_up_btn = Button(volume_x, button_y, 45, button_height, "+", lambda: self.core.adjust_volume(1), (0, 100, 0), (0, 150, 0))
        self.volume_down_btn = Button(volume_x + 55, button_y, 45, button_height, "-", lambda: self.core.adjust_volume(-1), (100, 0, 0), (150, 0, 0))
        
        self.all_buttons = self.buttons + [self.volume_up_btn, self.volume_down_btn]
    
    def load_ims_file(self, file_path):
        data = self.data_loader.load_ims_file(file_path)
        if data:
            self.core.set_metadata(self.data_loader.get_metadata())
            self.core.set_timeline(self.data_loader.get_timeline())
            self.media_handler.set_assets(data.get("assets", {}))
            
            title = self.core.metadata.get("title", "Immersion Reader")
            pygame.display.set_caption(f"Immersion Reader - {title}")
    
    def go_to_start(self):
        self.core.go_to_start()
        self.save_load.reset_current_save_slot()
        self.core.current_image_key = self.core.get_current_background_image_key()
        self.current_image_surface = self.media_handler.load_image(self.core.current_image_key)
        self.previous_image_surface = None
        self.core.is_transitioning = False
        self.core.is_text_fading = False
        self.core.image_switched = False
        self.core.current_image_index = -1
    
    def show_save_dialog(self):
        self.core.current_mode = "save"
        self.save_buttons = []
        
        for i in range(self.save_load.save_slots):
            x = 60 + (i % 5) * 180
            y = 140 + (i // 5) * 110
            btn = Button(x, y, 160, 100, f"槽位 {i+1}", lambda slot=i: self.confirm_save(slot), (60, 60, 60), (100, 100, 100))
            self.save_buttons.append(btn)
    
    def show_load_dialog(self):
        self.core.current_mode = "load"
        self.load_buttons = []
        
        for i in range(self.save_load.save_slots):
            x = 60 + (i % 5) * 180
            y = 140 + (i // 5) * 110
            btn = Button(x, y, 160, 100, f"槽位 {i+1}", lambda slot=i: self.confirm_load(slot), (60, 60, 60), (100, 100, 100))
            self.load_buttons.append(btn)
    
    def confirm_save(self, slot):
        if slot in self.save_load.get_save_info():
            self.confirm_dialog = ConfirmDialog(
                "确认覆盖",
                f"槽位 {slot+1} 已有存档，是否覆盖？",
                lambda: self.execute_save(slot),
                lambda: self.close_confirm_dialog()
            )
        else:
            self.execute_save(slot)
    
    def confirm_load(self, slot):
        if slot in self.save_load.get_save_info():
            self.confirm_dialog = ConfirmDialog(
                "确认读取",
                f"是否读取槽位 {slot+1} 的存档？",
                lambda: self.execute_load(slot),
                lambda: self.close_confirm_dialog()
            )
        else:
            self.close_confirm_dialog()
    
    def execute_save(self, slot):
        if self.save_load.save_to_slot(slot, self.core.current_segment_index):
            self.core.show_message(f"已保存到槽位 {slot+1} (第{self.core.current_segment_index + 1}页)")
            self.core.current_mode = "normal"
        else:
            self.core.show_message("保存失败")
        self.close_confirm_dialog()
    
    def execute_load(self, slot):
        success, saved_index = self.save_load.load_from_slot(slot)
        if success and self.core.timeline and 0 <= saved_index < len(self.core.timeline):
            self.core.current_segment_index = saved_index
            self.core.current_image_key = self.core.get_current_background_image_key()
            self.current_image_surface = self.media_handler.load_image(self.core.current_image_key)
            self.previous_image_surface = None
            self.core.is_transitioning = False
            self.core.is_text_fading = False
            self.core.image_switched = False
            self.core.current_image_index = -1
            self.core.auto_timer = 0
            self.core.skip_timer = 0
            self.core.is_playing = False
            self.core.is_auto_play = False
            self.core.is_skip_mode = False
            self.core.show_message(f"已读取槽位 {slot+1} (第{saved_index + 1}页)")
            self.core.current_mode = "normal"
            
            self.screen.fill(self.core.BLACK)
            self.draw()
            pygame.display.flip()
        else:
            self.core.show_message("读取失败")
        self.close_confirm_dialog()
    
    def close_confirm_dialog(self):
        self.confirm_dialog = None
    
    def draw_save_dialog(self):
        self.screen.fill(self.core.BLACK)
        
        title_surface = self.core.font.render("选择存档槽位", True, self.core.WHITE)
        self.screen.blit(title_surface, (self.width/2 - title_surface.get_width()/2, 40))
        
        hint_surface = self.core.small_font.render("点击槽位进行存档，ESC返回", True, self.core.GRAY)
        self.screen.blit(hint_surface, (self.width/2 - hint_surface.get_width()/2, 85))
        
        for btn in self.save_buttons:
            btn.draw(self.screen, self.core.button_font)
        
        for i in range(self.save_load.save_slots):
            x = 60 + (i % 5) * 180
            y = 140 + (i // 5) * 110
            
            if i in self.save_load.get_save_info():
                info = self.save_load.get_save_info()[i]
                
                timestamp_surface = self.core.small_font.render(info['timestamp'], True, (255, 200, 100))
                self.screen.blit(timestamp_surface, (x + 5, y + 30))
                
                page_info = f"第{self.save_load.get_slot_page(i)}页"
                page_surface = self.core.small_font.render(page_info, True, (100, 200, 255))
                self.screen.blit(page_surface, (x + 5, y + 55))
            else:
                empty_surface = self.core.small_font.render("[空]", True, (80, 80, 80))
                self.screen.blit(empty_surface, (x + 5, y + 30))
        
        if self.confirm_dialog:
            self.confirm_dialog.draw(self.screen, self.core.font, self.core.small_font)
        
        pygame.display.flip()
    
    def draw_load_dialog(self):
        self.screen.fill(self.core.BLACK)
        
        title_surface = self.core.font.render("选择读取槽位", True, self.core.WHITE)
        self.screen.blit(title_surface, (self.width/2 - title_surface.get_width()/2, 40))
        
        hint_surface = self.core.small_font.render("点击槽位进行读档，ESC返回", True, self.core.GRAY)
        self.screen.blit(hint_surface, (self.width/2 - hint_surface.get_width()/2, 85))
        
        for btn in self.load_buttons:
            btn.draw(self.screen, self.core.button_font)
        
        for i in range(self.save_load.save_slots):
            x = 60 + (i % 5) * 180
            y = 140 + (i // 5) * 110
            
            if i in self.save_load.get_save_info():
                info = self.save_load.get_save_info()[i]
                
                timestamp_surface = self.core.small_font.render(info['timestamp'], True, (255, 200, 100))
                self.screen.blit(timestamp_surface, (x + 5, y + 30))
                
                page_info = f"第{self.save_load.get_slot_page(i)}页"
                page_surface = self.core.small_font.render(page_info, True, (100, 200, 255))
                self.screen.blit(page_surface, (x + 5, y + 55))
            else:
                empty_surface = self.core.small_font.render("[空]", True, (80, 80, 80))
                self.screen.blit(empty_surface, (x + 5, y + 30))
        
        if self.confirm_dialog:
            self.confirm_dialog.draw(self.screen, self.core.font, self.core.small_font)
        
        pygame.display.flip()
    
    def update(self):
        new_image_key = self.core.check_image_transition(lambda image_key: None)
        if new_image_key:
            self.previous_image_surface = self.current_image_surface
            self.current_image_surface = self.media_handler.load_image(new_image_key)
        
        self.core.update(lambda image_key: None)
        
        if not self.core.first_music_completed:
            if not self.media_handler.is_audio_playing():
                self.core.first_music_completed = True
                self.media_handler.play_audio("sad_music")
    
    def draw(self):
        self.core.draw(self.screen, self.current_image_surface, self.previous_image_surface)
        
        button_bg = pygame.Surface((self.width, 70), pygame.SRCALPHA)
        pygame.draw.rect(button_bg, (0, 0, 0, 200), (0, 0, self.width, 70))
        self.screen.blit(button_bg, (0, self.height - 70))
        
        for btn in self.all_buttons:
            btn.draw(self.screen, self.core.button_font)
        
        pygame.display.flip()
    
    def next_segment(self):
        self.core.next_segment()
        segment = self.core.timeline[self.core.current_segment_index]
        if "image" in segment:
            self.current_image_surface = self.media_handler.load_image(segment["image"])
    
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if self.confirm_dialog:
            if self.confirm_dialog.handle_event(event):
                return
        
        if self.core.current_mode == "save":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.core.current_mode = "normal"
            
            for btn in self.save_buttons:
                btn.handle_event(event)
            return
        
        if self.core.current_mode == "load":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.core.current_mode = "normal"
            
            for btn in self.load_buttons:
                btn.handle_event(event)
            return
        
        if self.core.is_recall_mode:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_r:
                    self.core.toggle_recall_mode()
                elif event.key == pygame.K_UP:
                    self.core.adjust_recall_scroll(-40)
                elif event.key == pygame.K_DOWN:
                    self.core.adjust_recall_scroll(40)
                elif event.key == pygame.K_PAGEUP:
                    self.core.adjust_recall_scroll(-200)
                elif event.key == pygame.K_PAGEDOWN:
                    self.core.adjust_recall_scroll(200)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.core.adjust_recall_scroll(-40)
                elif event.button == 5:
                    self.core.adjust_recall_scroll(40)
                elif event.button == 1:
                    self.core.toggle_recall_mode()
            
            return
        
        for btn in self.all_buttons:
            if btn.handle_event(event):
                return
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.core.toggle_play_pause()
            elif event.key == pygame.K_m:
                self.core.toggle_auto_play()
            elif event.key == pygame.K_s:
                self.core.toggle_skip_mode()
            elif event.key == pygame.K_h:
                self.go_to_start()
            elif event.key == pygame.K_r:
                self.core.toggle_recall_mode()
            elif event.key == pygame.K_UP:
                self.core.adjust_volume(1)
            elif event.key == pygame.K_DOWN:
                self.core.adjust_volume(-1)
            elif event.key == pygame.K_LEFT:
                self.core.adjust_auto_speed(-1)
            elif event.key == pygame.K_RIGHT:
                self.core.adjust_auto_speed(1)
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            if mouse_y < self.height - 70:
                self.next_segment()
    
    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                self.handle_event(event)
            
            if self.core.is_recall_mode:
                self.core.draw_recall_mode(self.screen)
            elif self.core.current_mode == "save":
                self.draw_save_dialog()
            elif self.core.current_mode == "load":
                self.draw_load_dialog()
            else:
                self.update()
                self.draw()
            
            clock.tick(60)


if __name__ == "__main__":
    player = ImmersionPlayer()
    player.run()
