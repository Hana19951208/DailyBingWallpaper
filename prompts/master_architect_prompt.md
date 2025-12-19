# Role: Senior Python Architect & System Designer

## 🎯 Objective
Design and implement a **production-grade, multi-source wallpaper aggregation platform** ("DailyWallpaperHub"). 
The system must automatically fetch daily wallpapers from multiple providers (Bing, Unsplash), generate AI-driven visible stories, archive them persistently on GitHub, and deploy a responsive gallery via GitHub Pages.

## 🧠 Core Design Philosophy (The "Why" & "How")
Your implementation must adhere to the following architectural principles derived from real-world iterations:

1.  **Configuration-Driven Architecture (Scalability)**:
    *   **Do NOT** hardcode data sources. Use `config/sources.yaml` to manage providers.
    *   This allows adding new sources (e.g., NASA, National Geographic) by simply editing a YAML file, without touching core logic.

2.  **Asynchronous & Non-Blocking Design (Performance)**:
    *   **Critical Rule**: The fetching process (downloading images) must be decoupled from the heavy AI generation process.
    *   Use a flag (e.g., `--skip-story`) for the initial fetch job to ensure immediate availability of images.
    *   Use a separate, asynchronous script (`generate_missing_stories.py`) to handle time-consuming LLM calls in the background.

3.  **Deployment-First Storage Strategy (Reliability)**:
    *   **Strict Rule**: All archived images/metadata MUST be stored inside `docs/wallpapers/` (not the root `wallpapers/`).
    *   **Reason**: GitHub Pages typically deploys from the `docs/` folder. Files outside this context result in 404 errors.
    *   **Pathing**: Use relative paths (`./wallpapers/...`) in auto-generated HTML/Markdown to ensure links work on both local previews and GitHub Pages.

4.  **Unified Data Schema (Maintainability)**:
    *   Standardize all downloaded files: `image.jpg`, `thumb.jpg` (400x225), `meta.json`, `story.md`.
    *   Create a consistent metadata structure in `meta.json` regardless of the source API.

## 🛠 Technical Specifications

### 1. Directory Structure Blueprint
```text
DailyWallpaperHub/
├── config/
│   └── sources.yaml          # Define enabled sources, API keys env names
├── docs/                     # GitHub Pages Deployment Root
│   ├── index.html            # Auto-generated Responsive Gallery
│   ├── style.css             # Dark/Light mode styles
│   └── wallpapers/           # DATA STORAGE (Critical for 404 access)
│       ├── bing/
│       │   └── YYYY-MM-DD/
│       └── unsplash/
│           └── YYYY-MM-DD/
├── scripts/
│   └── generate_missing_stories.py  # Async AI Story Generator
├── src/
│   ├── update_readme.py      # Generates README table
│   └── update_gallery.py     # Generates docs/index.html
├── .github/workflows/daily.yml # Two-stage job: Fetch -> Generate Story
├── fetch_bing_wallpaper.py
├── fetch_unsplash_wallpaper.py
└── README.md
```

### 2. Workflow Automation (GitHub Actions)
Design the CI/CD pipeline with two distinct jobs:
*   **Job 1 (Fast)**: Run fetchers with `--skip-story`. Commit & Push immediately. (User sees new image instantly).
*   **Job 2 (Slow)**: Depends on Job 1. Run `generate_missing_stories.py`. Commit & Push updates. (AI stories appear later).

### 3. README & Documentation Standards
The `README.md` must be auto-updated and follow this premium layout:
*   **Header**: Project Name + Dynamic Badges (Build Status, Pages Status).
*   **Feature Grid**: Highlight Multi-source, Async AI, Weird-push, Gallery.
*   **Visual Index**: A dynamic table with **Date** as rows and **Sources** as columns (Bing | Unsplash).
*   **Quick Start**: Clear commands for local dev and batch fetching history.

## 🚫 "Pitfalls to Avoid" (Lessons Learned)
*   **The 404 Trap**: Never store deployment assets outside the `docs/` folder if deploying from `docs/`.
*   **The "Blocker"**: Never let a 30-second LLM call block the daily wallpaper update.
*   **The "Hardcode"**: Never write `if source == 'bing'` in core update logic. Iterate through configs instead.
*   **The "Path Hell"**: Always use `pathlib` with absolute path calculations relative to `__file__` to avoid CWD issues.

## 📝 Task
Based on the above architecture, please generate the initial project structure and key scripts. Start by defining `config/sources.yaml` and the base `fetcher` abstract logic.
