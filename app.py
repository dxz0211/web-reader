import os
import json
from datetime import datetime
from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory

app = Flask(__name__)

# ============================================================
# 路径常量
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
IMAGES_DIR = os.path.join(DATA_DIR, "images")
AUDIO_DIR = os.path.join(DATA_DIR, "audio")
SAVEDATA_DIR = os.path.join(BASE_DIR, "savedata")

for d in [DATA_DIR, SAVEDATA_DIR]:
    os.makedirs(d, exist_ok=True)

# ============================================================
# 辅助函数
# ============================================================
def list_files(directory, extensions=None):
    if not os.path.exists(directory):
        return []
    files = []
    for f in os.listdir(directory):
        if extensions:
            if any(f.lower().endswith(ext) for ext in extensions):
                files.append(f)
        else:
            files.append(f)
    return sorted(files)

# ============================================================
# 页面路由
# ============================================================
@app.route("/")
def index():
    return redirect(url_for("player_page"))

@app.route("/editor")
def editor_page():
    return render_template("editor.html")

@app.route("/player")
def player_page():
    return render_template("player.html")

@app.route("/help")
def help_page():
    return render_template("help.html")

# ============================================================
# 数据 API
# ============================================================
@app.route("/api/files")
def api_files():
    files = [f for f in os.listdir(DATA_DIR) if f.endswith(".ims")]
    return jsonify(sorted(files))

@app.route("/api/load")
def api_load():
    filename = request.args.get("file", "")
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "file not found"}), 404
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data)
    except json.JSONDecodeError:
        return jsonify({"error": "invalid json"}), 400

@app.route("/data/<path:filename>")
def serve_data_file(filename):
    """提供 data/ 目录下的静态资源（图片/音频）"""
    return send_from_directory(DATA_DIR, filename)


@app.route("/api/save", methods=["POST"])
def api_save():
    data = request.get_json()
    if not data:
        return jsonify({"error": "invalid json"}), 400
    title = data.get("metadata", {}).get("title", "untitled")
    safe_title = "".join(c for c in title if c.isalnum() or c in " _-").strip() or "untitled"
    filename = f"{safe_title}.ims"
    filepath = os.path.join(DATA_DIR, filename)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return jsonify({"status": "ok", "filename": filename})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/assets/images")
def api_assets_images():
    return jsonify(list_files(IMAGES_DIR, extensions=[".jpg", ".jpeg", ".png", ".gif"]))

@app.route("/api/assets/audios")
def api_assets_audios():
    return jsonify(list_files(AUDIO_DIR, extensions=[".mp3", ".wav", ".ogg"]))

@app.route("/api/save_progress", methods=["POST"])
def api_save_progress():
    body = request.get_json()
    if not body:
        return jsonify({"error": "invalid request"}), 400
    slot = body.get("slot")
    if slot is None or not (0 <= slot <= 9):
        return jsonify({"error": "slot must be 0-9"}), 400
    save_data = {
        "slot": slot,
        "filename": body.get("filename", ""),
        "segment_index": body.get("segment_index", 0),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    try:
        filepath = os.path.join(SAVEDATA_DIR, f"save_{slot}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/load_progress")
def api_load_progress():
    slot = request.args.get("slot", type=int)
    if slot is None or not (0 <= slot <= 9):
        return jsonify({"error": "slot must be 0-9"}), 400
    filepath = os.path.join(SAVEDATA_DIR, f"save_{slot}.json")
    if not os.path.exists(filepath):
        return jsonify({"error": "no save data"}), 404
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data)
    except (json.JSONDecodeError, Exception) as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/list_progress")
def api_list_progress():
    result = []
    for slot in range(10):
        filepath = os.path.join(SAVEDATA_DIR, f"save_{slot}.json")
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                result.append(data)
            except:
                result.append({"slot": slot, "error": "corrupted"})
        else:
            result.append(None)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)