# 角色：资深 Python 架构师 & 系统设计师

## 🎯 目标
设计并实现一个**生产级、多源壁纸聚合平台** ("DailyWallpaperHub")。
该系统必须能够从多个提供商（Bing、Unsplash）自动抓取每日壁纸，生成 AI 驱动的视觉故事，在 GitHub 上进行持久化归档，并通过 GitHub Pages 部署响应式画廊。

## 🧠 核心设计哲学 ("Why" & "How")
你的实现必须遵循以下源自实战迭代的架构原则：

1.  **配置驱动架构 (高扩展性)**:
    *   **禁止**硬编码数据源。使用 `config/sources.yaml` 管理提供商。
    *   这允许通过简单编辑 YAML 文件来添加新源（例如 NASA、国家地理），而无需修改核心逻辑。

2.  **异步与非阻塞设计 (高性能)**:
    *   **关键规则**: 抓取过程（下载图片）必须与繁重的 AI 生成过程解耦。
    *   在初始抓取任务中使用标志（例如 `--skip-story`）以确保图片立即可用。
    *   使用独立的异步脚本（`generate_missing_stories.py`）在后台处理耗时的 LLM 调用。

3.  **部署优先的存储策略 (高可靠性)**:
    *   **严格规则**: 所有归档的图片/元数据必须存储在 `docs/wallpapers/` 内部（而不是根目录 `wallpapers/`）。
    *   **原因**: GitHub Pages 通常从 `docs/` 文件夹部署。此上下文之外的文件会导致 404 错误。
    *   **路径**: 在自动生成的 HTML/Markdown 中使用相对路径（`./wallpapers/...`），以确保链接在本地预览和 GitHub Pages 上都能正常工作。

4.  **统一数据模式 (可维护性)**:
    *   标准化所有下载的文件：`image.jpg`、`thumb.jpg` (400x225)、`meta.json`、`story.md`。
    *   无论来源 API 如何，都在 `meta.json` 中创建一致的元数据结构。

## 🛠 技术规范

### 1. 目录结构蓝图
```text
DailyWallpaperHub/
├── config/
│   └── sources.yaml          # 定义启用的源、API 密钥环境变量名
├── docs/                     # GitHub Pages 部署根目录
│   ├── index.html            # 自动生成的响应式画廊
│   ├── style.css             # 深色/浅色模式样式
│   └── wallpapers/           # 数据存储 (解决 404 的关键)
│       ├── bing/
│       │   └── YYYY-MM-DD/
│       └── unsplash/
│           └── YYYY-MM-DD/
├── scripts/
│   └── generate_missing_stories.py  # 异步 AI 故事生成器
├── src/
│   ├── update_readme.py      # 生成 README 表格
│   └── update_gallery.py     # 生成 docs/index.html
├── .github/workflows/daily.yml # 两阶段任务：抓取 -> 生成故事
├── fetch_bing_wallpaper.py
├── fetch_unsplash_wallpaper.py
└── README.md
```

### 2. 工作流自动化 (GitHub Actions)
设计包含两个不同 Job 的 CI/CD 管道：
*   **Job 1 (快速)**: 运行带有 `--skip-story` 的抓取器。立即提交并推送。（用户能立即看到新图片）。
*   **Job 2 (慢速)**: 依赖于 Job 1。运行 `generate_missing_stories.py`。提交并推送更新。（AI 故事稍后出现）。

### 3. README & 文档标准
`README.md` 必须自动更新并遵循此高级布局：
*   **页眉**: 项目名称 + 动态徽章（构建状态、Pages 状态）。
*   **特性网格**: 突出显示多源、异步 AI、微信推送、画廊。
*   **可视化索引**: 一个动态表格，以 **日期** 为行，**来源** 为列（Bing | Unsplash）。
*   **快速开始**: 清晰的本地开发和批量抓取历史记录的命令。

## 🚫 "避坑指南" (经验教训)
*   **404 陷阱**: 如果从 `docs/` 部署，切勿将部署资源存储在 `docs/` 文件夹之外。
*   **阻塞者**: 切勿让 30 秒的 LLM 调用阻塞每日壁纸更新。
*   **硬编码**: 切勿在核心更新逻辑中写 `if source == 'bing'`。遍历配置代替。
*   **路径地狱**: 始终使用带有相对于 `__file__` 的绝对路径计算的 `pathlib`，以避免 CWD 问题。

## 📝 任务
基于上述架构，请生成初始项目结构和关键脚本。从定义 `config/sources.yaml` 和基础 `fetcher` 抽象逻辑开始。
