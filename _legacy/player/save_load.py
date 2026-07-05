import os
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class SaveLoadManager:
    def __init__(self, save_slots=10):
        self.save_slots = save_slots
        self.savedata_dir = os.path.join(PROJECT_ROOT, "savedata")
        os.makedirs(self.savedata_dir, exist_ok=True)
        self.current_save_slot = -1
        self.save_info = {}
        self.load_save_info()
    
    def load_save_info(self):
        try:
            info_file = os.path.join(self.savedata_dir, "save_info.txt")
            if os.path.exists(info_file):
                with open(info_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if '=' in line:
                            parts = line.split('=', 1)
                            if len(parts) >= 2:
                                slot_str, timestamp = parts[0], parts[1]
                                slot = int(slot_str)
                                timestamp = timestamp.rstrip('=')
                                self.save_info[slot] = {
                                    'timestamp': timestamp
                                }
        except Exception as e:
            print(f"加载存档信息失败: {e}")
    
    def save_info_to_file(self):
        try:
            info_file = os.path.join(self.savedata_dir, "save_info.txt")
            with open(info_file, 'w', encoding='utf-8') as f:
                for slot in sorted(self.save_info.keys()):
                    info = self.save_info[slot]
                    f.write(f"{slot}={info['timestamp']}\n")
        except Exception as e:
            print(f"保存存档信息失败: {e}")
    
    def get_slot_page(self, slot):
        save_file = os.path.join(self.savedata_dir, f"save_{slot}.txt")
        if not os.path.exists(save_file):
            return 0
        try:
            with open(save_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    return int(content) + 1
        except Exception as e:
            print(f"读取槽位{slot}页码失败: {e}")
        return 0
    
    def save_to_slot(self, slot, current_segment_index):
        if slot < 0 or slot >= self.save_slots:
            return False
        
        save_file = os.path.join(self.savedata_dir, f"save_{slot}.txt")
        try:
            with open(save_file, 'w', encoding='utf-8') as f:
                f.write(str(current_segment_index))
            
            self.save_info[slot] = {
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            self.save_info_to_file()
            self.current_save_slot = slot
            return True
        except Exception as e:
            print(f"保存到槽位{slot}失败: {e}")
            return False
    
    def load_from_slot(self, slot):
        if slot < 0 or slot >= self.save_slots:
            return False, None
        
        save_file = os.path.join(self.savedata_dir, f"save_{slot}.txt")
        if not os.path.exists(save_file):
            return False, None
        
        try:
            with open(save_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    saved_index = int(content)
                    self.current_save_slot = slot
                    return True, saved_index
        except Exception as e:
            print(f"从槽位{slot}加载失败: {e}")
        return False, None
    
    def clear_slot(self, slot):
        if slot < 0 or slot >= self.save_slots:
            return False
        
        save_file = os.path.join(self.savedata_dir, f"save_{slot}.txt")
        try:
            if os.path.exists(save_file):
                os.remove(save_file)
            if slot in self.save_info:
                del self.save_info[slot]
                self.save_info_to_file()
            if self.current_save_slot == slot:
                self.current_save_slot = -1
            return True
        except Exception as e:
            print(f"清除槽位{slot}失败: {e}")
            return False
    
    def get_save_info(self):
        return self.save_info
    
    def get_current_save_slot(self):
        return self.current_save_slot
    
    def reset_current_save_slot(self):
        self.current_save_slot = -1
