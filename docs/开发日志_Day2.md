# 开发日志 — Day2

**日期**：2025-07-15
**项目**：Immersion Reader Web 版（沉浸式阅读创作平台）
**状态**：Day1 基础稳固 → Day2 编辑器核心完成 + 播放器/样式整合 → 全流程链路贯通

---

## 今日完成

| 模块 | 完成内容 | 完成度 |
|------|----------|--------|
| 编辑器 editor.html | 三栏布局（元数据/段落时间轴/资源面板）、段落动态增删、表单填充、保存/打开、文件上传 | 95% |
| 编辑器文件上传 | 新增后端 `/api/upload` + 前端上传按钮，支持从本地导入图片/音频到 `data/` | 100% |
| 播放器改造 player.html | 移除内联 `<style>`，全面引用 `style.css`，添加导航栏，修复 DOM 引用 | 100% |
| 帮助页面 help.html | 填充完整使用说明（编辑器教程、播放器教程、快捷键、文件格式、技术说明） | 100% |
| 样式整合 | 三个页面（编辑器/播放器/帮助）统一使用 `style.css` 深蓝主题 | 100% |
| Bug 修复 | 修复 4 个关键 Bug（见下方 Bug 修复清单） | 100% |

## Bug 修复清单

| 编号 | 问题 | 根因 | 修复方式 |
|------|------|------|----------|
| 2-1 | 点击添加按钮后，上一段已输入的文字消失 | `addSegment()` 直接 push 新数据后 `renderTimeline()` 重写 HTML，DOM 中的编辑内容未回写到 `segments` 数组 | `addSegment()` 改为先调用 `collectSegmentsFromDOM()` 回写再 push |
| 2-2 | 页面无法下滑，添加的段落2看不见 | `.editor-container` 使用 `overflow: hidden` 限制了整体高度，中栏无独立滚动 | 为 `.editor-panel` 添加 `overflow-y: auto; max-height: calc(100vh - 56px)` |
| 1 | 无法从本地硬盘导入音频、图片 | 缺少文件上传 UI 和后端接口 | 后端新增 `POST /api/upload`，编辑器右栏新增 `📤 上传图片` / `📤 上传音频` 按钮 |
| 3 | "打开"按钮加载后只有 Toast，无法跳转播放器 | `openFileModal` 文件列表只有点击加载编辑功能，无跳转播放入口 | 每个文件旁新增 `▶ 播放` 按钮，点击新标签页打开播放器 |

## 当前项目结构

```
immersion_reader/
├── app.py                          # Flask 后端（10个API，含 /api/upload）
├── requirements.txt                # flask
├── templates/
│   ├── editor.html                 # ✅ 完整编辑器（95%）
│   ├── player.html                 # ✅ 完整播放器（引用 style.css）
│   └── help.html                   # ✅ 完整帮助页面
├── static/
│   └── style.css                   # ✅ 完整样式（B完成，已整合）
├── data/
│   ├── sample.ims                  # ✅ 戴望舒《雨巷》（13段）
│   ├── images/                     # lantern.jpg, rain_street.jpg
│   └── audio/                      # 2首MP3
├── savedata/                       # ✅ 存档系统（10槽位）
├── docs/
│   ├── 规格说明书_v1.0.md          # ✅ 完整规格
│   ├── 开发日志_Day1.md            # ✅
│   └── 开发日志_Day2.md            # ✅ （本文件）
└── _legacy/                        # 旧版 Pygame 归档
```

## 新增 API

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/upload` | POST | 接收 multipart 文件，按扩展名存入 `data/images/` 或 `data/audio/` |

## 编辑器完整功能清单

| 功能 | 状态 |
|------|------|
| 三栏布局（元数据 / 段落时间轴 / 资源面板） | ✅ |
| 元数据编辑（标题、作者、创作者、简介） | ✅ |
| 段落动态增删（至少保留1段） | ✅ |
| 段落文字编辑（textarea） | ✅ |
| 段落起始时间 + 持续时长（数字输入） | ✅ |
| 背景图下拉选择（从 API 实时读取） | ✅ |
| 背景音乐下拉选择（从 API 实时读取） | ✅ |
| 切换效果选择（交叉淡入淡出/淡入/无效果） | ✅ |
| 保存为 `.ims`（`POST /api/save`） | ✅ |
| 打开已有 `.ims`（弹窗选文件 → 填充表单） | ✅ |
| 文件列表每项旁"▶ 播放"按钮（跳转播放器） | ✅ |
| 从本地导入图片/音频（上传按钮） | ✅ |
| Ctrl+S 快捷键保存 | ✅ |
| Toast 消息提示 | ✅ |

## 播放器改造详情

| 改造项 | 说明 |
|--------|------|
| 移除内联 `<style>` | 原 ~70 行内联样式删除，完全依赖外部 `style.css` |
| 添加导航栏 | `<nav class="navbar">` 可返回编辑器和帮助 |
| 容器类名 | `#player-container` 添加 `class="player-container"` |
| 背景图元素 | `#bg-image` 添加 `class="player-background active"` |
| 元数据显示 | `#info-bar` 改为 `class="player-metadata"` |
| 进度指示器 | `#progress-text` 添加 `class="player-progress"` |
| 文字覆盖层 | 结构改为 `.player-text-overlay > .player-text-box` |
| 控制栏 | `#controls` 改为 `class="player-controls"` |
| 弹窗 | `modal-box` 改为 `modal-dialog`，`.show` 改为 `.hidden` 切换 |
| JS 适配 | `txtOv` 引用从 `#text-overlay` 改为 `#text-box` |

## 待完成（Day3）

| 任务 | 责任 | 优先级 |
|------|------|--------|
| 全流程联调测试（编辑器→保存→播放器）（T6） | A + AI | P0 |
| 编辑器保存验证（T1-T2） | A + AI | P0 |
| 播放器播放验证（T3-T5） | A + AI | P0 |
| 过渡效果验证（T9-T10） | A + AI | P0 |
| README.md | B | P1 |
| 论文第1-2章 | C | P0 |
| 编辑器"打开"后加载 toast 增加跳转播放器入口 | A | P2 |

## 启动方式

```bash
cd "C:\Users\车越\Desktop\python code\immersion_reader"
python app.py
```
- 编辑器：http://localhost:5000/editor
- 播放器：http://localhost:5000/player?file=sample.ims
- 帮助：http://localhost:5000/help

---

**文档版本**：v1.0（Day2）
