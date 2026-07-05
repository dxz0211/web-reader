import pygame
import os
import tkinter as tk
from tkinter import filedialog
from .editor_core import EditorCore

class EditorFileOps:
    def __init__(self, core: EditorCore):
        self.core = core
    
    def new_file(self):
        self.core.current_file_path = None
        self.core.is_modified = False
        self.core.text_segments = []
        self.core.images = []
        self.core.audio_file = None
        self.core.audio_duration = 0
        self.core.timeline_tracks = {
            "text": [],
            "image": [],
            "audio": []
        }
        self.core.selected_segment_index = -1
        self.core.selected_node = {
            "track": None,
            "index": -1
        }
        self.core.show_message("已创建新文件")
        pygame.display.set_caption(self.core.get_window_title())
    
    def open_file(self):
        root = tk.Tk()
        root.withdraw()
        
        file_path = filedialog.askopenfilename(
            title="打开项目文件",
            filetypes=[("项目文件", "*.json"), ("所有文件", "*.*")]
        )
        
        if file_path:
            try:
                import json
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.core.current_file_path = file_path
                self.core.text_segments = data.get("text_segments", [])
                self.core.images = data.get("images", [])
                self.core.audio_file = data.get("audio_file", None)
                self.core.audio_duration = data.get("audio_duration", 0)
                self.core.timeline_tracks = data.get("timeline_tracks", {
                    "text": [],
                    "image": [],
                    "audio": []
                })
                self.core.is_modified = False
                
                if file_path not in self.core.recent_files:
                    self.core.recent_files.insert(0, file_path)
                    if len(self.core.recent_files) > 10:
                        self.core.recent_files.pop()
                
                self.core.show_message(f"已打开文件: {os.path.basename(file_path)}")
                pygame.display.set_caption(self.core.get_window_title())
            except Exception as e:
                self.core.show_message(f"打开文件失败: {str(e)}")
    
    def open_recent_file(self, file_path):
        if os.path.exists(file_path):
            try:
                import json
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.core.current_file_path = file_path
                self.core.text_segments = data.get("text_segments", [])
                self.core.images = data.get("images", [])
                self.core.audio_file = data.get("audio_file", None)
                self.core.audio_duration = data.get("audio_duration", 0)
                self.core.timeline_tracks = data.get("timeline_tracks", {
                    "text": [],
                    "image": [],
                    "audio": []
                })
                self.core.is_modified = False
                
                self.core.recent_files.remove(file_path)
                self.core.recent_files.insert(0, file_path)
                
                self.core.show_message(f"已打开文件: {os.path.basename(file_path)}")
                pygame.display.set_caption(self.core.get_window_title())
            except Exception as e:
                self.core.show_message(f"打开文件失败: {str(e)}")
        else:
            self.core.show_message(f"文件不存在: {file_path}")
    
    def save_file(self):
        if self.core.current_file_path:
            self._save_to_file(self.core.current_file_path)
        else:
            self.save_as_file()
    
    def save_as_file(self):
        root = tk.Tk()
        root.withdraw()
        
        file_path = filedialog.asksaveasfilename(
            title="保存项目文件",
            defaultextension=".json",
            filetypes=[("项目文件", "*.json"), ("所有文件", "*.*")]
        )
        
        if file_path:
            self._save_to_file(file_path)
    
    def _save_to_file(self, file_path):
        try:
            import json
            
            data = {
                "text_segments": self.core.text_segments,
                "images": self.core.images,
                "audio_file": self.core.audio_file,
                "audio_duration": self.core.audio_duration,
                "timeline_tracks": self.core.timeline_tracks
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.core.current_file_path = file_path
            self.core.is_modified = False
            
            if file_path not in self.core.recent_files:
                self.core.recent_files.insert(0, file_path)
                if len(self.core.recent_files) > 10:
                    self.core.recent_files.pop()
            
            self.core.show_message(f"已保存文件: {os.path.basename(file_path)}")
            pygame.display.set_caption(self.core.get_window_title())
        except Exception as e:
            self.core.show_message(f"保存文件失败: {str(e)}")
    
    def get_recent_files_menu(self):
        items = []
        if not self.core.recent_files:
            items.append({"name": "(无最近文件)", "action": None})
        else:
            for i, file_path in enumerate(self.core.recent_files[:5]):
                items.append({
                    "name": f"{i+1}. {os.path.basename(file_path)}",
                    "action": lambda path=file_path: self.open_recent_file(path)
                })
        return items