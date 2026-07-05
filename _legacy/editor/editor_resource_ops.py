import pygame
import os
import tkinter as tk
from tkinter import filedialog
from .editor_core import EditorCore

class EditorResourceOps:
    def __init__(self, core: EditorCore):
        self.core = core
    
    def add_image(self):
        root = tk.Tk()
        root.withdraw()
        
        file_path = filedialog.askopenfilename(
            title="选择图片文件",
            filetypes=[("图片文件", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        
        if file_path:
            try:
                img = pygame.image.load(file_path)
                width, height = img.get_size()
                
                image_info = {
                    "path": file_path,
                    "name": os.path.basename(file_path),
                    "width": width,
                    "height": height,
                    "pygame_image": img
                }
                
                self.core.images.append(image_info)
                self.core.is_modified = True
                self.core.show_message(f"已添加图片: {os.path.basename(file_path)}")
            except Exception as e:
                self.core.show_message(f"添加图片失败: {str(e)}")
    
    def add_audio(self):
        root = tk.Tk()
        root.withdraw()
        
        file_path = filedialog.askopenfilename(
            title="选择音频文件",
            filetypes=[("音频文件", "*.mp3 *.wav *.ogg *.mid")]
        )
        
        if file_path:
            try:
                pygame.mixer.music.load(file_path)
                duration = pygame.mixer.Sound(file_path).get_length()
                
                self.core.audio_file = {
                    "path": file_path,
                    "name": os.path.basename(file_path),
                    "duration": duration
                }
                self.core.audio_duration = duration
                self.core.is_modified = True
                self.core.show_message(f"已添加音频: {os.path.basename(file_path)} ({duration:.1f}s)")
            except Exception as e:
                self.core.show_message(f"添加音频失败: {str(e)}")