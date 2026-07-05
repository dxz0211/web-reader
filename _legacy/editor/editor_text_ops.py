import pygame
import tkinter as tk
from .editor_core import EditorCore

class EditorTextOps:
    def __init__(self, core: EditorCore):
        self.core = core
    
    def undo(self):
        self.core.show_message("撤销功能待实现")
    
    def redo(self):
        self.core.show_message("重做功能待实现")
    
    def add_text_segment(self):
        self.core.text_segments.append("新文本段落")
        self.core.is_modified = True
        self.core.show_message("已添加文本段落")
        pygame.display.set_caption(self.core.get_window_title())
    
    def copy_text(self):
        if self.core.is_editing_text and self.core.editing_text:
            try:
                root = tk.Tk()
                root.withdraw()
                root.clipboard_clear()
                root.clipboard_append(self.core.editing_text)
                root.update()
                root.destroy()
                self.core.show_message("已复制文本")
            except Exception as e:
                self.core.show_message(f"复制失败: {str(e)}")
    
    def paste_text(self):
        if self.core.is_editing_text:
            try:
                root = tk.Tk()
                root.withdraw()
                text = root.clipboard_get()
                root.destroy()
                if text:
                    self.core.editing_text = (self.core.editing_text[:self.core.cursor_pos] + 
                                            text + 
                                            self.core.editing_text[self.core.cursor_pos:])
                    self.core.cursor_pos += len(text)
                    self.core.is_modified = True
                    self.core.show_message("已粘贴文本")
            except Exception as e:
                self.core.show_message(f"粘贴失败: {str(e)}")
    
    def cut_text(self):
        if self.core.is_editing_text and self.core.editing_text:
            try:
                root = tk.Tk()
                root.withdraw()
                root.clipboard_clear()
                root.clipboard_append(self.core.editing_text)
                root.update()
                root.destroy()
                self.core.editing_text = ""
                self.core.cursor_pos = 0
                self.core.is_modified = True
                self.core.show_message("已剪切文本")
            except Exception as e:
                self.core.show_message(f"剪切失败: {str(e)}")
    
    def delete_selected_text(self):
        if 0 <= self.core.selected_segment_index < len(self.core.text_segments):
            del self.core.text_segments[self.core.selected_segment_index]
            self.core.selected_segment_index = -1
            self.core.is_modified = True
            self.core.show_message("已删除选中文本")
            pygame.display.set_caption(self.core.get_window_title())