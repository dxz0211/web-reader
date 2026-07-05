import os
import sys
from pathlib import Path

# 获取项目根目录（tests 文件夹的上级目录）
project_root = Path(__file__).parent.parent.resolve()
# 添加到 sys.path
sys.path.append(str(project_root))

from player.data_loader import DataLoader

def run_basic_test():
    """基础功能测试"""
    print("=== 基础加载测试 ===")
    
    loader = DataLoader()
    # 使用项目根目录构建绝对路径
    data_path = os.path.join(project_root, "data", "sample.ims")
    result = loader.load_ims_file(data_path)
    
    if result:
        print("✅ 基础加载测试通过")
        return True
    else:
        print("❌ 基础加载测试失败")
        return False

def run_metadata_test():
    """元数据测试"""
    print("\n=== 元数据测试 ===")
    
    loader = DataLoader()
    # 使用项目根目录构建绝对路径
    data_path = os.path.join(project_root, "data", "sample.ims")
    loader.load_ims_file(data_path)
    metadata = loader.get_metadata()
    
    if metadata and metadata['title'] == "雨巷":
        print("✅ 元数据测试通过")
        print(f"   标题: {metadata['title']}")
        print(f"   作者: {metadata['author']}")
        return True
    else:
        print("❌ 元数据测试失败")
        return False

def run_timeline_test():
    """时间轴测试"""
    print("\n=== 时间轴测试 ===")
    
    loader = DataLoader()
    # 使用项目根目录构建绝对路径
    data_path = os.path.join(project_root, "data", "sample.ims")
    loader.load_ims_file(data_path)
    timeline = loader.get_timeline()
    
    if timeline and len(timeline) == 2:
        print("✅ 时间轴测试通过")
        for segment in timeline:
            print(f"   段落{segment['segment_id']}: {segment['text'][:10]}...")
        return True
    else:
        print("❌ 时间轴测试失败")
        return False

# 新增：测试无效文件场景
def run_invalid_file_test():
    """测试无效文件加载"""
    print("\n=== 无效文件测试 ===")
    loader = DataLoader()
    # 测试不存在的文件
    invalid_path = os.path.join(project_root, "data", "invalid.ims")
    result = loader.load_ims_file(invalid_path)
    
    if not result:
        print("✅ 无效文件测试通过")
        return True
    else:
        print("❌ 无效文件测试失败")
        return False

if __name__ == "__main__":
    print("开始运行IMS数据加载器测试...\n")
    
    # 包含新增的无效文件测试
    tests = [run_basic_test, run_metadata_test, run_timeline_test, run_invalid_file_test]
    passed = 0
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n=== 测试总结 ===")
    print(f"通过: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("🎉 所有测试通过！数据加载器工作正常。")
    else:
        print("⚠️  部分测试失败，请检查代码。")