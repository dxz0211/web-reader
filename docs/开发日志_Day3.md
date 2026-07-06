"# 开发日志 — Day3

**日期**：2025-07-16
**项目**：Immersion Reader Web 版（沉浸式阅读创作平台）
**状态**：Day2 核心功能完成 → Day3 Bug 修复 + 体验优化 → 达到答辩演示标准

---

## 今日完成

| 模块 | 完成内容 | 完成度 |
|------|----------|--------|
| 播放器 Bug 修复 | 存档空槽位、项目隔离、上下段切换、图片/音乐去重切换 | 100% |
| 编辑器 Bug 修复 | 新建 .ims 图片不显示（别名匹配）、"打开"逻辑回归纯编辑 | 100% |
| 编辑器体验优化 | 资源面板改为项目级显示（非全局） | 100% |
| 规格说明书更新 | v1.2 发布，同步最新功能 | 100% |
| Git 提交 | 首次提交所有代码到仓库 | 100% |

## Bug 修复清单

| 编号 | 问题 | 根因 | 修复方式 | 影响文件 |
|------|------|------|----------|----------|
| P0-1 | 存档空槽位无法保存 | `openSlotGrid` 点击回调要求 `info` 非空才执行 `doSave`，但保存应允许写入空槽位 | 移除 `save` 模式对 `info` 的依赖 | player.html |
| P0-2 | 不同项目存档混在一起 | 存档文件名仅含槽位号，未区分项目 | 存档文件名改为 `save_{filename}_{slot}.json`，API 增加 `filename` 参数 | app.py, player.html |
| P0-3 | 播放中上下段切换混乱 | `doNext/doPrev` 重置计时器时未跳转到目标段落的起点时间 | 计算目标段落的 `start_time`，通过 `pauseAccum = -targetStartTime` 实现时间跳转 | player.html |
| P0-4 | 新建 .ims 图片无法显示 | 编辑器 `timeline[].background` 存的是文件名，但 `assets.images` 的 key 是去扩展名的别名 | `saveFile` 中 `timeline[].background` 改为存别名 | editor.html |
| P0-5 | 相同图片/音乐切换时仍触发动画和音乐重播 | `showSeg` 无条件切换背景图和音乐 | 添加 `prevBgKey`/`prevMuKey` 变量，只在值变化时切换 | player.html |
| P0-6 | 编辑器"打开"弹窗含播放按钮，逻辑混乱 | Day2 错误添加了跳转播放器入口 | 移除弹窗中的"▶ 播放"按钮，回归纯编辑逻辑 | editor.html |

## 体验优化

| 编号 | 优化项 | 说明 |
|------|--------|------|
| P1-1 | 资源面板项目级显示 | 新建项目时显示"暂无图片/音频"，打开 .ims 时只显示该项目 assets 中引用的资源，上传按钮追加到项目资源池。不再读取全局 `data/` 目录 |

## 当前项目结构

```
immersion_reader/
├── app.py                          # Flask 后端（10个API，含项目隔离存档）
├── requirements.txt                # flask
├── templates/
│   ├── editor.html                 # ✅ 完整编辑器（资源项目级显示）
│   ├── player.html                 # ✅ 完整播放器（Bug 全部修复）
│   └── help.html                   # ✅ 完整帮助页面
├── static/
│   └── style.css                   # ✅ 完整样式（深蓝主题）
├── data/
│   ├── sample.ims                  # ✅ 戴望舒《雨巷》（13段）
│   ├── images/
│   └── audio/
├── savedata/                       # ✅ 项目隔离存档系统
├── docs/
│   ├── 规格说明书_v1.2.md          # ✅ 最新规格
│   ├── 开发日志_Day1.md            # ✅
│   ├── 开发日志_Day2.md            # ✅
│   └── 开发日志_Day3.md            # ✅ （本文件）
└── _legacy/                        # 旧版 Pygame 归档
```

## 技术要点总结

### 存档项目隔离

```
旧：savedata/save_0.json ~ save_9.json（所有项目共用）
新：savedata/save_{filename}_{slot}.json（每个项目独立 10 个槽位）
```

### 播放器切换优化

```javascript
// 图片/音乐只在变化时切换，避免相同内容闪烁
if (bgKey !== prevBgKey) { /* 切换背景图 */ }
if (muKey !== prevMuKey) { /* 切换音乐 */ }
// 文字始终更新
```

### 编辑器别名存储

```javascript
// 保存时：文件名 → 别名
timeline[].background = filename.replace(/\.[^.]+$/, ''); // "lantern.jpg" → "lantern"
assets.images["lantern"] = "data/images/lantern.jpg";
```

## 待完成（Day4）

| 任务 | 责任 | 优先级 |
|------|------|--------|
| 全流程端到端测试（T1-T12） | A + AI | P0 |
| 论文第3-4章 | C | P0 |
| 答辩 PPT 准备 | 全员 | P0 |
| README.md | B | P1 |

## 启动方式

```bash
cd "C:\\Users\\车越\\Desktop\\python code\\immersion_reader"
python app.py
```
- 编辑器：http://localhost:5000/editor
- 播放器：http://localhost:5000/player?file=sample.ims
- 帮助：http://localhost:5000/help

---

**文档版本**：v1.0（Day3）
"