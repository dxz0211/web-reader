import os
import pygame
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class MediaHandler:
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.current_audio = None
        self.assets = {}
    
    def set_assets(self, assets):
        self.assets = assets
    
    def play_audio(self, audio_key):
        if audio_key in self.assets.get("audios", {}):
            audio_path = self.assets["audios"][audio_key]
            if not os.path.isabs(audio_path):
                audio_path = os.path.join(self.data_loader.project_root, audio_path)
            
            try:
                if self.current_audio:
                    pygame.mixer.music.stop()
                
                pygame.mixer.music.load(audio_path)
                pygame.mixer.music.play(-1)
                self.current_audio = audio_key
                return True
            except pygame.error as e:
                print(f"音频播放错误: {e}")
                return False
        return False
    
    def load_image(self, image_key, width=1000, height=600):
        if image_key in self.assets.get("images", {}):
            image_path = self.assets["images"][image_key]
            if not os.path.isabs(image_path):
                image_path = os.path.join(self.data_loader.project_root, image_path)
            
            try:
                image = pygame.image.load(image_path)
                image = pygame.transform.scale(image, (width, height))
                return image
            except pygame.error as e:
                print(f"图像加载错误: {e}")
                return None
        return None
    
    def stop_audio(self):
        pygame.mixer.music.stop()
        self.current_audio = None
    
    def pause_audio(self):
        pygame.mixer.music.pause()
    
    def unpause_audio(self):
        pygame.mixer.music.unpause()
    
    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)
    
    def get_current_audio(self):
        return self.current_audio
    
    def is_audio_playing(self):
        return pygame.mixer.music.get_busy()
