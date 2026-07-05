import pygame
from .editor_core import EditorCore

class EditorUI:
    def __init__(self, core: EditorCore):
        self.core = core
    
    def draw_menu_bar(self, screen, menus):
        pygame.draw.rect(screen, self.core.DARK_GRAY, self.core.menu_bar_rect)
        pygame.draw.line(screen, self.core.GRAY, (0, 40), (self.core.width, 40), 1)
        
        for menu in menus:
            menu_rect = menu["rect"]
            menu_text = self.core.title_font.render(menu["name"], True, self.core.WHITE)
            text_rect = menu_text.get_rect(center=menu_rect.center)
            screen.blit(menu_text, text_rect)
    
    def draw_toolbar(self, screen, toolbar_buttons):
        pygame.draw.rect(screen, self.core.LIGHT_GRAY, self.core.toolbar_rect)
        pygame.draw.line(screen, self.core.GRAY, (0, 90), (self.core.width, 90), 1)
        
        for btn in toolbar_buttons:
            btn.draw(screen, self.core.small_font)
    
    def draw_text_area(self, screen, text_segments, selected_segment_index, 
                      is_editing_text, editing_segment_index, editing_text, cursor_pos):
        pygame.draw.rect(screen, self.core.WHITE, self.core.text_area_rect)
        pygame.draw.rect(screen, self.core.GRAY, self.core.text_area_rect, 1)
        
        for i, segment in enumerate(text_segments):
            segment_rect = segment["rect"]
            text = segment["text"]
            
            if i == selected_segment_index:
                pygame.draw.rect(screen, self.core.LIGHT_BLUE, segment_rect)
            
            if i == editing_segment_index and is_editing_text:
                display_text = editing_text
                
                if cursor_pos < len(display_text):
                    prefix = display_text[:cursor_pos]
                    suffix = display_text[cursor_pos:]
                else:
                    prefix = display_text
                    suffix = ""
                
                if prefix:
                    prefix_surface = self.core.font.render(prefix, True, self.core.BLACK)
                    screen.blit(prefix_surface, (segment_rect.x + 5, segment_rect.y + 5))
                
                cursor_x = segment_rect.x + 5
                if prefix:
                    cursor_x += prefix_surface.get_width()
                
                pygame.draw.line(screen, self.core.BLACK, 
                               (cursor_x, segment_rect.y + 5), 
                               (cursor_x, segment_rect.y + 25), 2)
                
                if suffix:
                    suffix_surface = self.core.font.render(suffix, True, self.core.BLACK)
                    screen.blit(suffix_surface, (cursor_x, segment_rect.y + 5))
            else:
                if text:
                    text_surface = self.core.font.render(text, True, self.core.BLACK)
                    screen.blit(text_surface, (segment_rect.x + 5, segment_rect.y + 5))
    
    def draw_timeline_area(self, screen, timeline_items, selected_timeline_index):
        pygame.draw.rect(screen, self.core.LIGHT_GRAY, self.core.timeline_area_rect)
        pygame.draw.line(screen, self.core.GRAY, (0, 650), (self.core.width, 650), 1)
        
        for i, item in enumerate(timeline_items):
            item_rect = item["rect"]
            time_text = item["time"]
            
            if i == selected_timeline_index:
                pygame.draw.rect(screen, self.core.LIGHT_BLUE, item_rect)
            
            time_surface = self.core.small_font.render(time_text, True, self.core.BLACK)
            text_rect = time_surface.get_rect(center=item_rect.center)
            screen.blit(time_surface, text_rect)
    
    def draw_resource_panel(self, screen, resource_items, selected_resource_index):
        pygame.draw.rect(screen, self.core.LIGHT_GRAY, self.core.resource_panel_rect)
        pygame.draw.line(screen, self.core.GRAY, (900, 90), (900, 650), 1)
        
        for i, item in enumerate(resource_items):
            item_rect = item["rect"]
            name = item["name"]
            
            if i == selected_resource_index:
                pygame.draw.rect(screen, self.core.LIGHT_BLUE, item_rect)
            
            name_surface = self.core.small_font.render(name, True, self.core.BLACK)
            text_rect = name_surface.get_rect(center=item_rect.center)
            screen.blit(name_surface, text_rect)
    
    def draw_status_bar(self, screen, current_mode, current_file_path, is_modified):
        pygame.draw.rect(screen, self.core.DARK_GRAY, self.core.status_bar_rect)
        pygame.draw.line(screen, self.core.GRAY, (0, 760), (self.core.width, 760), 1)
        
        mode_text = f"模式: {current_mode}"
        mode_surface = self.core.small_font.render(mode_text, True, self.core.WHITE)
        screen.blit(mode_surface, (10, 765))
        
        if current_file_path:
            file_text = f"文件: {current_file_path}"
            if is_modified:
                file_text += " *"
            file_surface = self.core.small_font.render(file_text, True, self.core.WHITE)
            screen.blit(file_surface, (150, 765))
        else:
            file_surface = self.core.small_font.render("文件: 未打开", True, self.core.WHITE)
            screen.blit(file_surface, (150, 765))
