import pygame
import sys
from .editor_core import EditorCore

class EditorTimelineOps:
    def __init__(self, core: EditorCore):
        self.core = core
    
    def add_node_to_timeline(self, track_type=None, time=0):
        if track_type is None:
            track_type = self.core.selected_track
            time = 0
        
        if track_type == "text" and self.core.selected_segment_index >= 0:
            segment = self.core.text_segments[self.core.selected_segment_index]
            node = {
                "time": time,
                "duration": 5,
                "name": f"文本_{self.core.selected_segment_index + 1}",
                "content": segment
            }
            self.core.timeline_tracks[track_type].append(node)
            self.core.is_modified = True
            self.core.show_message(f"已添加文本节点到{track_type}轨道")
        elif track_type == "image" and self.core.selected_image_index >= 0:
            image_info = self.core.images[self.core.selected_image_index]
            node = {
                "time": time,
                "duration": 5,
                "name": image_info["name"],
                "path": image_info["path"]
            }
            self.core.timeline_tracks[track_type].append(node)
            self.core.is_modified = True
            self.core.show_message(f"已添加图片节点到{track_type}轨道")
        elif track_type == "audio" and self.core.audio_file is not None:
            node = {
                "time": time,
                "duration": self.core.audio_file["duration"],
                "name": self.core.audio_file["name"],
                "path": self.core.audio_file["path"]
            }
            self.core.timeline_tracks[track_type].append(node)
            self.core.is_modified = True
            self.core.show_message(f"已添加音频节点到{track_type}轨道")
        else:
            self.core.show_message(f"请先选择{track_type}类型的资源")
    
    def delete_selected_node(self):
        track_type = self.core.selected_node["track"]
        node_index = self.core.selected_node["index"]
        if track_type is not None and node_index >= 0:
            del self.core.timeline_tracks[track_type][node_index]
            self.core.selected_node = {"track": None, "index": -1}
            self.core.is_modified = True
            self.core.show_message(f"已删除{track_type}轨道上的节点")
    
    def preview(self):
        self.core.show_message("预览功能待实现")
    
    def stop_preview(self):
        self.core.show_message("停止预览功能待实现")
    
    def show_help(self):
        self.core.show_message("使用指南功能待实现")
    
    def show_about(self):
        self.core.show_message("沉浸式阅读编辑器 v1.0")
    
    def exit_editor(self):
        pygame.quit()
        sys.exit()