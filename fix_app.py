with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '    return sorted(files)\n\n# ============================================================\n# 页面路由'

new = '''    return sorted(files)

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

# ============================================================
# 页面路由'''

if old in content:
    content = content.replace(old, new, 1)
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('OK')
else:
    print('NOT FOUND')
    # debug: show what's actually there
    idx = content.find('return sorted(files)')
    if idx >= 0:
        print(repr(content[idx:idx+120]))
