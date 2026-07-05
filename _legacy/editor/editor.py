import pygame
import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

pygame.init()
pygame.mixer.init()

from player.ui_components import Button
from .editor_core import EditorCore
from .editor_ui import EditorUI
from .editor_events import EditorEvents
from .editor_file_ops import EditorFileOps
from .editor_text_ops import EditorTextOps
from .editor_resource_ops import EditorResourceOps
from .editor_timeline_ops import EditorTimelineOps


class ImmersionEditor:
    def __init__(self):
        self.core = EditorCore()
        self.screen = pygame.display.set_mode((self.core.width, self.core.height))
        pygame.display.set_caption(self.core.get_window_title())
        
        self.ui = EditorUI(self.core)
        self.events = EditorEvents(self.core)
        self.file_ops = EditorFileOps(self.core)
        self.text_ops = EditorTextOps(self.core)
        self.resource_ops = EditorResourceOps(self.core)
        self.timeline_ops = EditorTimelineOps(self.core)
        
        self.init_menu_items()
        self.init_toolbar_buttons()
    
    def init_menu_items(self):
        menu_y = 8
        menu_height = 24
        
        self.menus = [
            {
                "name": "文件",
                "items": [
                    {"name": "新建", "action": self.new_file, "shortcut": "Ctrl+N"},
                    {"name": "打开", "action": self.open_file, "shortcut": "Ctrl+O"},
                    {"name": "保存", "action": self.save_file, "shortcut": "Ctrl+S"},
                    {"name": "另存为", "action": self.save_as_file, "shortcut": "Ctrl+Shift+S"},
                    {"name": "-", "separator": True},
                    {"name": "最近文件", "submenu": self.get_recent_files_menu()},
                    {"name": "-", "separator": True},
                    {"name": "退出", "action": self.exit_editor, "shortcut": "Alt+F4"}
                ]
            },
            {
                "name": "编辑",
                "items": [
                    {"name": "撤销", "action": self.undo, "shortcut": "Ctrl+Z"},
                    {"name": "重做", "action": self.redo, "shortcut": "Ctrl+Y"},
                    {"name": "-", "separator": True},
                    {"name": "添加文本段落", "action": self.add_text_segment, "shortcut": "Ctrl+T"},
                    {"name": "删除选中文本", "action": self.delete_selected_text, "shortcut": "Delete"},
                    {"name": "-", "separator": True},
                    {"name": "添加图片", "action": self.add_image, "shortcut": "Ctrl+I"},
                    {"name": "添加音频", "action": self.add_audio, "shortcut": "Ctrl+A"}
                ]
            },
            {
                "name": "预览",
                "items": [
                    {"name": "预览", "action": self.preview, "shortcut": "F5"},
                    {"name": "停止预览", "action": self.stop_preview, "shortcut": "Esc"}
                ]
            },
            {
                "name": "帮助",
                "items": [
                    {"name": "使用指南", "action": self.show_help, "shortcut": "F1"},
                    {"name": "关于", "action": self.show_about, "shortcut": ""}
                ]
            }
        ]
        
        menu_x = 10
        for menu in self.menus:
            menu["rect"] = pygame.Rect(menu_x, menu_y, 80, menu_height)
            menu_x += 85
    
    def init_toolbar_buttons(self):
        button_y = 55
        button_height = 30
        button_width = 70
        spacing = 10
        start_x = 20
        
        self.toolbar_buttons = [
            Button(start_x, button_y, button_width, button_height, "新建", self.new_file, self.core.DARK_GRAY, self.core.LIGHT_GRAY),
            Button(start_x + (button_width + spacing) * 1, button_y, button_width, button_height, "打开", self.open_file, self.core.DARK_GRAY, self.core.LIGHT_GRAY),
            Button(start_x + (button_width + spacing) * 2, button_y, button_width, button_height, "保存", self.save_file, self.core.DARK_GRAY, self.core.LIGHT_GRAY),
            Button(start_x + (button_width + spacing) * 3, button_y, button_width, button_height, "预览", self.preview, self.core.BLUE, self.core.LIGHT_BLUE),
        ]
    
    def get_recent_files_menu(self):
        return self.file_ops.get_recent_files_menu()
    
    def new_file(self):
        self.file_ops.new_file()
    
    def open_file(self):
        self.file_ops.open_file()
    
    def open_recent_file(self, file_path):
        self.file_ops.open_recent_file(file_path)
    
    def save_file(self):
        self.file_ops.save_file()
    
    def save_as_file(self):
        self.file_ops.save_as_file()
    
    def undo(self):
        self.text_ops.undo()
    
    def redo(self):
        self.text_ops.redo()
    
    def add_text_segment(self):
        self.text_ops.add_text_segment()
    
    def copy_text(self):
        self.text_ops.copy_text()
    
    def paste_text(self):
        self.text_ops.paste_text()
    
    def cut_text(self):
        self.text_ops.cut_text()
    
    def delete_selected_text(self):
        self.text_ops.delete_selected_text()
    
    def add_image(self):
        self.resource_ops.add_image()
    
    def add_audio(self):
        self.resource_ops.add_audio()
    
    def preview(self):
        self.timeline_ops.preview()
    
    def stop_preview(self):
        self.timeline_ops.stop_preview()
    
    def show_help(self):
        self.timeline_ops.show_help()
    
    def show_about(self):
        self.timeline_ops.show_about()
    
    def exit_editor(self):
        self.timeline_ops.exit_editor()
    
    def add_node_to_timeline(self, track_type=None, time=0):
        self.timeline_ops.add_node_to_timeline(track_type, time)
    
    def delete_selected_node(self):
        self.timeline_ops.delete_selected_node()
    
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.events.handle_quit(self.exit_editor)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(f"鼠标点击位置: {event.pos}")
            print(f"文本区域位置: {self.core.text_area_rect}")
            print(f"资源区域位置: {self.core.resource_area_rect}")
            print(f"时间轴区域位置: {self.core.timeline_area_rect}")
        
        if self.events.handle_toolbar_buttons(event, self.toolbar_buttons):
            print("工具栏按钮处理了事件")
        
        if event.type == pygame.KEYDOWN:
            self.events.handle_keydown(event, self)
        
        if event.type == pygame.TEXTINPUT:
            self.events.handle_textinput(event, self)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.events.handle_mousebuttondown(event, self)
        
        if event.type == pygame.MOUSEBUTTONUP:
            self.events.handle_mousebuttonup(event)
        
        if event.type == pygame.MOUSEMOTION:
            self.events.handle_mousemotion(event)
    
    def draw(self):
        self.screen.fill(self.core.WHITE)
        
        self.ui.draw_menu_bar(self.screen, self.menus)
        self.ui.draw_toolbar(self.screen, self.toolbar_buttons)
        
        self.draw_text_area()
        self.draw_resource_area()
        self.draw_timeline_area()
        
        self.ui.draw_status_bar(self.screen, self.core.current_mode, 
                               self.core.current_file_path, self.core.is_modified)
        
        if self.core.message_timer > 0:
            message_surface = self.core.small_font.render(self.core.current_message, True, self.core.BLACK)
            message_rect = message_surface.get_rect(center=(self.core.width // 2, self.core.height - 60))
            pygame.draw.rect(self.screen, self.core.SEMI_TRANSPARENT_WHITE, 
                           message_rect.inflate(20, 10), border_radius=5)
            self.screen.blit(message_surface, message_rect)
        
        pygame.display.flip()
    
    def draw_text_area(self):
        pygame.draw.rect(self.screen, self.core.WHITE, self.core.text_area_rect)
        pygame.draw.rect(self.screen, self.core.GRAY, self.core.text_area_rect, 2)
        
        title_text = self.core.title_font.render("文本区域", True, self.core.BLACK)
        self.screen.blit(title_text, (self.core.text_area_rect.x + 10, self.core.text_area_rect.y + 10))
        
        y_offset = 40
        for i, segment in enumerate(self.core.text_segments):
            if self.core.is_editing_text and i == self.core.editing_segment_index:
                bg_color = self.core.LIGHT_BLUE
                pygame.draw.rect(self.screen, bg_color, (
                    self.core.text_area_rect.x + 10,
                    self.core.text_area_rect.y + 10 + y_offset,
                    self.core.text_area_rect.width - 20,
                    30
                ), border_radius=5)
                
                editing_text = f"{i+1}. {self.core.editing_text}"
                segment_text = self.core.font.render(editing_text, True, self.core.WHITE)
                self.screen.blit(segment_text, (self.core.text_area_rect.x + 20, self.core.text_area_rect.y + 15 + y_offset))
                
                cursor_x = self.core.text_area_rect.x + 20 + self.core.font.size(editing_text[:self.core.cursor_pos + 3])[0]
                cursor_y = self.core.text_area_rect.y + 15 + y_offset
                cursor_end_y = cursor_y + self.core.font.size("A")[1]
                pygame.draw.line(self.screen, self.core.WHITE, (cursor_x, cursor_y), (cursor_x, cursor_end_y), 2)
            else:
                bg_color = self.core.LIGHT_BLUE if i == self.core.selected_segment_index else self.core.WHITE
                text_color = self.core.WHITE if i == self.core.selected_segment_index else self.core.BLACK
                
                segment_rect = pygame.Rect(
                    self.core.text_area_rect.x + 10,
                    self.core.text_area_rect.y + 10 + y_offset,
                    self.core.text_area_rect.width - 20,
                    30
                )
                
                pygame.draw.rect(self.screen, bg_color, segment_rect, border_radius=5)
                
                segment_text = self.core.font.render(f"{i+1}. {segment}", True, text_color)
                self.screen.blit(segment_text, (segment_rect.x + 10, segment_rect.y + 5))
            
            y_offset += 35
        
        if len(self.core.text_segments) == 0:
            empty_text = self.core.small_font.render("点击添加文本段落或使用快捷键Ctrl+T", True, self.core.GRAY)
            self.screen.blit(empty_text, (
                self.core.text_area_rect.x + 10,
                self.core.text_area_rect.y + 50
            ))
    
    def draw_resource_area(self):
        pygame.draw.rect(self.screen, self.core.WHITE, self.core.resource_area_rect)
        pygame.draw.rect(self.screen, self.core.GRAY, self.core.resource_area_rect, 2)
        
        title_text = self.core.title_font.render("资源区域", True, self.core.BLACK)
        self.screen.blit(title_text, (self.core.resource_area_rect.x + 10, self.core.resource_area_rect.y + 10))
        
        y_offset = 40
        for i, image_info in enumerate(self.core.images):
            row = i // 3
            col = i % 3
            image_rect = pygame.Rect(
                self.core.resource_area_rect.x + 10 + col * 200,
                self.core.resource_area_rect.y + 10 + y_offset + row * 120,
                180,
                110
            )
            
            bg_color = self.core.LIGHT_BLUE if i == self.core.selected_image_index else self.core.LIGHT_GRAY
            pygame.draw.rect(self.screen, bg_color, image_rect, border_radius=5)
            pygame.draw.rect(self.screen, self.core.GRAY, image_rect, 2, border_radius=5)
            
            try:
                img = image_info["pygame_image"]
                img_width, img_height = img.get_size()
                scale = min((image_rect.width - 20) / img_width, (image_rect.height - 40) / img_height)
                new_width = int(img_width * scale)
                new_height = int(img_height * scale)
                resized_img = pygame.transform.scale(img, (new_width, new_height))
                
                img_x = image_rect.x + (image_rect.width - new_width) // 2
                img_y = image_rect.y + 10
                self.screen.blit(resized_img, (img_x, img_y))
            except Exception as e:
                error_text = self.core.small_font.render("图片加载失败", True, self.core.RED)
                text_rect = error_text.get_rect(center=(image_rect.centerx, image_rect.centery - 10))
                self.screen.blit(error_text, text_rect)
            
            name_text = self.core.small_font.render(image_info["name"], True, self.core.BLACK)
            name_x = image_rect.x + (image_rect.width - name_text.get_width()) // 2
            name_y = image_rect.y + image_rect.height - 25
            self.screen.blit(name_text, (name_x, name_y))
        
        if self.core.audio_file:
            audio_rect = pygame.Rect(
                self.core.resource_area_rect.x + 10,
                self.core.resource_area_rect.y + 10 + y_offset + 2 * 120,
                180,
                110
            )
            
            pygame.draw.rect(self.screen, self.core.LIGHT_GREEN, audio_rect, border_radius=5)
            pygame.draw.rect(self.screen, self.core.GRAY, audio_rect, 2, border_radius=5)
            
            name_text = self.core.font.render(self.core.audio_file["name"], True, self.core.BLACK)
            name_rect = name_text.get_rect(center=(audio_rect.centerx, audio_rect.centery - 10))
            self.screen.blit(name_text, name_rect)
    
    def draw_timeline_area(self):
        pygame.draw.rect(self.screen, self.core.LIGHT_GRAY, self.core.timeline_area_rect)
        pygame.draw.rect(self.screen, self.core.GRAY, self.core.timeline_area_rect, 2)
        
        title_text = self.core.title_font.render("时间轴", True, self.core.BLACK)
        self.screen.blit(title_text, (self.core.timeline_area_rect.x + 10, self.core.timeline_area_rect.y + 10))
        
        timeline_x = self.core.timeline_area_rect.x + 100
        timeline_y = self.core.timeline_area_rect.y + 40
        timeline_width = self.core.timeline_area_rect.width - 110
        
        pygame.draw.line(self.screen, self.core.GRAY, 
                        (timeline_x, timeline_y), 
                        (timeline_x, timeline_y + 3 * self.core.track_height), 2)
        
        for i in range(0, self.core.timeline_duration + 1, 5):
            x = timeline_x + i * self.core.timeline_scale
            if x <= timeline_x + timeline_width:
                pygame.draw.line(self.screen, self.core.GRAY, (x, timeline_y), (x, timeline_y + 5), 1)
                time_text = self.core.small_font.render(f"{i}s", True, self.core.BLACK)
                self.screen.blit(time_text, (x - 10, timeline_y - 20))
        
        track_start_y = timeline_y
        for track_index, (track_type, nodes) in enumerate(self.core.timeline_tracks.items()):
            track_y = track_start_y + track_index * self.core.track_height
            
            track_rect = pygame.Rect(
                self.core.timeline_area_rect.x + 10,
                track_y,
                80,
                self.core.track_height
            )
            
            bg_color = self.core.LIGHT_BLUE if track_type == self.core.selected_track else self.core.LIGHT_GRAY
            pygame.draw.rect(self.screen, bg_color, track_rect, border_radius=3)
            pygame.draw.rect(self.screen, self.core.GRAY, track_rect, 1, border_radius=3)
            
            track_name = self.core.small_font.render(track_type, True, self.core.BLACK)
            track_name_rect = track_name.get_rect(center=track_rect.center)
            self.screen.blit(track_name, track_name_rect)
            
            track_content_rect = pygame.Rect(
                timeline_x,
                track_y,
                timeline_width,
                self.core.track_height
            )
            pygame.draw.rect(self.screen, self.core.WHITE, track_content_rect, border_radius=3)
            pygame.draw.rect(self.screen, self.core.GRAY, track_content_rect, 1, border_radius=3)
            
            for node in nodes:
                node_x = timeline_x + (node["time"] + self.core.timeline_offset) * self.core.timeline_scale
                node_width = node["duration"] * self.core.timeline_scale
                
                if node_x + node_width > timeline_x and node_x < timeline_x + timeline_width:
                    node_rect = pygame.Rect(
                        node_x,
                        track_y + 2,
                        node_width,
                        self.core.track_height - 4
                    )
                    
                    if (self.core.selected_node["track"] == track_type and 
                        nodes.index(node) == self.core.selected_node["index"]):
                        bg_color = self.core.LIGHT_BLUE
                    else:
                        bg_color = self.core.LIGHT_GREEN
                    
                    pygame.draw.rect(self.screen, bg_color, node_rect, border_radius=3)
                    pygame.draw.rect(self.screen, self.core.GRAY, node_rect, 1, border_radius=3)
                    
                    if node_width > 30:
                        name_text = self.core.small_font.render(node["name"], True, self.core.BLACK)
                        name_x = max(node_rect.x + 5, node_rect.x)
                        name_y = node_rect.y + (node_rect.height - name_text.get_height()) // 2
                        self.screen.blit(name_text, (name_x, name_y))
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                self.handle_event(event)
            
            self.core.update()
            self.draw()
            
            clock.tick(60)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    editor = ImmersionEditor()
    editor.run()