""# -*- coding: utf-8 -*-
# 临时脚本：在 app.py 中插入调试端点

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 在第 33 行（索引 32，即 '    return sorted(files)\n' 之后）插入调试端点
insert_code = '''
# ============================================================
# 调试端点：确认 Railway 上的文件目录结构（答辩后可删除）
# ============================================================
@app.route("/debug/paths")
def debug_paths():
    def safe_list(d):
        try:
            if os.path.isdir(d):
                return os.listdir(d)
            return ["目录不存在"]
        except Exception as e:
            return [str(e)]
    return {
        "BASE_DIR": BASE_DIR,
        "DATA_DIR": DATA_DIR,
        "DATA_EXISTS": os.path.isdir(DATA_DIR),
        "DATA_FILES": safe_list(DATA_DIR),
        "IMAGES_DIR": IMAGES_DIR,
        "IMAGES_EXISTS": os.path.isdir(IMAGES_DIR),
        "IMAGES_FILES": safe_list(IMAGES_DIR),
        "AUDIO_DIR": AUDIO_DIR,
        "AUDIO_EXISTS": os.path.isdir(AUDIO_DIR),
        "AUDIO_FILES": safe_list(AUDIO_DIR),
    }
'''

lines.insert(33, insert_code)

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('[OK] Debug endpoint inserted successfully!')"
