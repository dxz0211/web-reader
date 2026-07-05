import os
import json
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("DataLoader")

class DataLoader:
    def __init__(self):
        self.data = None  # 存储加载的完整数据
        self.project_root = self._get_project_root()  # 项目根目录

    def _get_project_root(self):
        """获取项目根目录（定位到data文件夹的上级目录）"""
        # 从当前文件（data_loader.py）向上查找项目根目录
        current_path = Path(__file__).resolve().parent
        # 假设项目根目录是当前文件的上级目录（根据实际结构调整）
        root = current_path.parent
        logger.info(f"自动识别项目根目录: {root}")
        return root

    def load_ims_file(self, file_path):
        """加载.ims文件，自动转换为基于项目根的绝对路径"""
        # 强制转换为绝对路径（优先使用项目根目录拼接）
        if not os.path.isabs(file_path):
            # 若传入相对路径，自动拼接项目根目录
            file_path = os.path.join(self.project_root, file_path)
        
        absolute_path = os.path.abspath(file_path)
        logger.info(f"尝试加载文件: {absolute_path}")

        # 检查文件是否存在
        if not os.path.exists(absolute_path):
            logger.error(f"文件不存在: {absolute_path}")
            return None
        if not os.path.isfile(absolute_path):
            logger.error(f"不是有效文件: {absolute_path}")
            return None

        # 读取并解析JSON
        try:
            with open(absolute_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            logger.info("文件加载成功")
            return self.data
        except json.JSONDecodeError:
            logger.error("文件格式错误（非 valid JSON）")
            return None
        except PermissionError:
            logger.error(f"无权限读取文件: {absolute_path}")
            return None
        except Exception as e:
            logger.error(f"加载失败: {str(e)}")
            return None

    def get_metadata(self):
        """获取元数据（加载文件后调用）"""
        if not self.data:
            logger.warning("未加载任何文件，无法获取元数据")
            return None
        return self.data.get('metadata', {})

    def get_timeline(self):
        """获取时间轴数据（加载文件后调用）"""
        if not self.data:
            logger.warning("未加载任何文件，无法获取时间轴")
            return None
        return self.data.get('timeline', [])