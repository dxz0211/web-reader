import pygame
from .editor_core import EditorCore

class EditorEvents:
    def __init__(self, core: EditorCore):
        self.core = core
    
    def handle_quit(self, exit_callback):
        exit_callback()
    
    def handle_toolbar_buttons(self, event, toolbar_buttons):
        for btn in toolbar_buttons:
            if btn.handle_event(event):
                return True
        return False
    
    def handle_keydown(self, event, editor):
        if self.core.is_editing_text:
            self._handle_text_editing_keys(event)
        else:
            self._handle_global_shortcuts(event, editor)
    
    def _handle_text_editing_keys(self, event):
        if event.key == pygame.K_ESCAPE:
            self._finish_editing()
        elif event.key == pygame.K_RETURN:
            self._finish_editing()
        elif event.key == pygame.K_BACKSPACE:
            if self.core.cursor_pos > 0:
                self.core.editing_text = (self.core.editing_text[:self.core.cursor_pos-1] + 
                                        self.core.editing_text[self.core.cursor_pos:])
                self.core.cursor_pos -= 1
                self.core.is_modified = True
        elif event.key == pygame.K_DELETE:
            if self.core.cursor_pos < len(self.core.editing_text):
                self.core.editing_text = (self.core.editing_text[:self.core.cursor_pos] + 
                                        self.core.editing_text[self.core.cursor_pos+1:])
                self.core.is_modified = True
        elif event.key == pygame.K_LEFT:
            self.core.cursor_pos = max(0, self.core.cursor_pos - 1)
        elif event.key == pygame.K_RIGHT:
            self.core.cursor_pos = min(len(self.core.editing_text), self.core.cursor_pos + 1)
        elif event.key == pygame.K_HOME:
            self.core.cursor_pos = 0
        elif event.key == pygame.K_END:
            self.core.cursor_pos = len(self.core.editing_text)
        elif event.mod & pygame.KMOD_CTRL:
            if event.key == pygame.K_c:
                editor.copy_text()
            elif event.key == pygame.K_v:
                editor.paste_text()
            elif event.key == pygame.K_x:
                editor.cut_text()
            elif event.key == pygame.K_a:
                self.core.cursor_pos = len(self.core.editing_text)
    
    def _handle_global_shortcuts(self, event, editor):
        if event.key == pygame.K_ESCAPE:
            editor.stop_preview()
        elif event.key == pygame.K_F5:
            editor.preview()
        elif event.key == pygame.K_F1:
            editor.show_help()
        elif event.mod & pygame.KMOD_CTRL:
            if event.key == pygame.K_n:
                editor.new_file()
            elif event.key == pygame.K_o:
                editor.open_file()
            elif event.key == pygame.K_s:
                if event.mod & pygame.KMOD_SHIFT:
                    editor.save_as_file()
                else:
                    editor.save_file()
            elif event.key == pygame.K_t:
                editor.add_text_segment()
            elif event.key == pygame.K_i:
                editor.add_image()
            elif event.key == pygame.K_a:
                editor.add_audio()
            elif event.key == pygame.K_z:
                editor.undo()
            elif event.key == pygame.K_y:
                editor.redo()
            elif event.key == pygame.K_e:
                editor.add_node_to_timeline()
        elif event.key == pygame.K_DELETE:
            if self.core.selected_node["track"] is not None:
                editor.delete_selected_node()
            else:
                editor.delete_selected_text()
    
    def handle_textinput(self, event, editor):
        if self.core.is_editing_text:
            text = event.text
            if text:
                self.core.editing_text = (self.core.editing_text[:self.core.cursor_pos] + 
                                        text + 
                                        self.core.editing_text[self.core.cursor_pos:])
                self.core.cursor_pos += len(text)
                self.core.is_modified = True
    
    def handle_mousebuttondown(self, event, editor):
        if event.button == 1:
            mouse_x, mouse_y = event.pos
            clicked_on_any_area = False
            
            if self._handle_text_area_click(mouse_x, mouse_y, editor):
                clicked_on_any_area = True
            
            if self._handle_resource_area_click(mouse_x, mouse_y):
                clicked_on_any_area = True
            
            if self._handle_timeline_area_click(mouse_x, mouse_y, editor):
                clicked_on_any_area = True
            
            if not clicked_on_any_area:
                self._reset_selection_state()
    
    def _handle_text_area_click(self, mouse_x, mouse_y, editor):
        if not self.core.text_area_rect.collidepoint(mouse_x, mouse_y):
            return False
        
        if self.core.is_editing_text and self.core.editing_segment_index >= 0:
            self.core.text_segments[self.core.editing_segment_index] = self.core.editing_text
        
        found_segment = False
        y_offset = 40
        for i, segment in enumerate(self.core.text_segments):
            segment_rect = pygame.Rect(
                self.core.text_area_rect.x + 10,
                self.core.text_area_rect.y + 10 + y_offset + i * 35,
                self.core.text_area_rect.width - 20,
                30
            )
            
            if segment_rect.collidepoint(mouse_x, mouse_y):
                self.core.is_editing_text = True
                self.core.editing_segment_index = i
                self.core.editing_text = segment
                self.core.cursor_pos = len(segment)
                self.core.selected_segment_index = i
                found_segment = True
                break
        
        if not found_segment:
            if not self.core.text_segments:
                editor.add_text_segment()
            
            last_index = len(self.core.text_segments) - 1
            self.core.is_editing_text = True
            self.core.editing_segment_index = last_index
            self.core.editing_text = self.core.text_segments[last_index]
            self.core.cursor_pos = len(self.core.editing_text)
            self.core.selected_segment_index = last_index
        
        return True
    
    def _handle_resource_area_click(self, mouse_x, mouse_y):
        if not self.core.resource_area_rect.collidepoint(mouse_x, mouse_y):
            return False
        
        y_offset = 40
        is_image_clicked = False
        
        for i in range(len(self.core.images)):
            image_rect = pygame.Rect(
                self.core.resource_area_rect.x + 10 + (i % 3) * 200,
                self.core.resource_area_rect.y + 10 + y_offset + (i // 3) * 120,
                180,
                110
            )
            if image_rect.collidepoint(mouse_x, mouse_y):
                self.core.selected_image_index = i
                is_image_clicked = True
        
        if not is_image_clicked and self.core.audio_file:
            audio_rect = pygame.Rect(
                self.core.resource_area_rect.x + 10,
                self.core.resource_area_rect.y + 10 + y_offset + 2 * 120,
                180,
                110
            )
            if audio_rect.collidepoint(mouse_x, mouse_y):
                self.core.selected_image_index = -1
        
        return True
    
    def _handle_timeline_area_click(self, mouse_x, mouse_y, editor):
        if not self.core.timeline_area_rect.collidepoint(mouse_x, mouse_y):
            return False
        
        timeline_x = self.core.timeline_area_rect.x + 100
        timeline_y = self.core.timeline_area_rect.y + 40
        timeline_width = self.core.timeline_area_rect.width - 110
        
        track_start_y = timeline_y
        for track_index, (track_type, nodes) in enumerate(self.core.timeline_tracks.items()):
            track_y = track_start_y + track_index * self.core.track_height
            track_rect = pygame.Rect(
                self.core.timeline_area_rect.x + 10,
                track_y,
                80,
                self.core.track_height
            )
            if track_rect.collidepoint(mouse_x, mouse_y):
                self.core.selected_track = track_type
                self.core.selected_node = {"track": None, "index": -1}
                return True
        
        self.core.selected_node = {"track": None, "index": -1}
        for track_index, (track_type, nodes) in enumerate(self.core.timeline_tracks.items()):
            track_y = track_start_y + track_index * self.core.track_height
            for node_index, node in enumerate(nodes):
                node_x = timeline_x + (node["time"] + self.core.timeline_offset) * self.core.timeline_scale
                node_width = node["duration"] * self.core.timeline_scale
                node_rect = pygame.Rect(
                    node_x,
                    track_y,
                    node_width,
                    self.core.track_height
                )
                if node_rect.collidepoint(mouse_x, mouse_y):
                    self.core.selected_node = {"track": track_type, "index": node_index}
                    self.core.is_dragging_node = True
                    self.core.drag_start_x = mouse_x
                    self.core.drag_start_time = node["time"]
                    return True
        
        for track_index, (track_type, nodes) in enumerate(self.core.timeline_tracks.items()):
            track_y = track_start_y + track_index * self.core.track_height
            track_rect = pygame.Rect(
                timeline_x,
                track_y,
                timeline_width,
                self.core.track_height
            )
            if track_rect.collidepoint(mouse_x, mouse_y):
                self.core.selected_track = track_type
                self.core.selected_node = {"track": None, "index": -1}
                click_time = (mouse_x - timeline_x) / self.core.timeline_scale - self.core.timeline_offset
                editor.add_node_to_timeline(track_type, max(0, click_time))
                return True
        
        return True
    
    def _reset_selection_state(self):
        if self.core.is_editing_text:
            self._finish_editing()
        self.core.selected_segment_index = -1
        self.core.selected_image_index = -1
        self.core.selected_node = {"track": None, "index": -1}
    
    def _finish_editing(self):
        if self.core.is_editing_text and self.core.editing_segment_index >= 0:
            self.core.text_segments[self.core.editing_segment_index] = self.core.editing_text
        self.core.is_editing_text = False
        self.core.editing_segment_index = -1
        self.core.editing_text = ""
        self.core.cursor_pos = 0
        self.core.is_modified = True
    
    def handle_mousebuttonup(self, event):
        if event.button == 1:
            self.core.is_dragging_node = False
    
    def handle_mousemotion(self, event):
        if self.core.is_dragging_node and self.core.selected_node["track"] is not None:
            mouse_x, mouse_y = event.pos
            timeline_x = self.core.timeline_area_rect.x + 100
            delta_x = mouse_x - self.core.drag_start_x
            delta_time = delta_x / self.core.timeline_scale
            track_type = self.core.selected_node["track"]
            node_index = self.core.selected_node["index"]
            new_time = max(0, self.core.drag_start_time + delta_time)
            self.core.timeline_tracks[track_type][node_index]["time"] = new_time
            self.core.is_modified = True
        elif self.core.timeline_area_rect.collidepoint(event.pos):
            mouse_x, mouse_y = event.pos
            timeline_y = self.core.timeline_area_rect.y + 40
            track_start_y = timeline_y
            for track_index, (track_type, nodes) in enumerate(self.core.timeline_tracks.items()):
                track_y = track_start_y + track_index * self.core.track_height
                track_rect = pygame.Rect(
                    self.core.timeline_area_rect.x + 10,
                    track_y,
                    self.core.timeline_area_rect.width - 10,
                    self.core.track_height
                )
                if track_rect.collidepoint(mouse_x, mouse_y):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    return
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)