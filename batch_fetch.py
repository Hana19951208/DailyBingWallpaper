#!/usr/bin/env python3
"""
批量抓取 2025 年 12 月的必应壁纸 (本地调用脚本)
"""

import os
import json
import requests
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image

# 导入主脚本的工具函数
import fetch_bing_wallpaper
from src.update_readme import update_readme
from src.update_gallery import update_gallery

BING_API = "https://www.bing.com/HPImageArchive.aspx"
BING_BASE = "https://www.bing.com"

def batch_fetch(target_month="2025-12"):
    print(f"🚀 开始批量抓取 {target_month} 的壁纸...")
    
    # 尝试抓取多页 (每页 8 张)
    # idx 0 是今天，idx 7 是 7 天前，以此类推
    # 我们抓取 idx 0-7, 8-15, 16-23 (如果支持)
    all_images = []
    for idx_start in [0, 8, 16]:
        params = {
            "format": "js",
            "idx": idx_start,
            "n": 8,
            "mkt": "zh-CN"
        }
        try:
            resp = requests.get(BING_API, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            all_images.extend(data.get("images", []))
        except Exception as e:
            print(f"⚠️ 无法获取 idx={idx_start} 的数据: {e}")

    fetch_bing_wallpaper.load_env()
    count = 0
    story_count = 0
    
    for img in all_images:
        start_date = img.get("startdate")
        if not start_date: continue
        
        date_str = f"{start_date[:4]}-{start_date[4:6]}-{start_date[6:8]}"
        
        # 只处理目标月份
        if not date_str.startswith(target_month):
            continue
            
        base_dir = Path("wallpapers") / date_str
        base_dir.mkdir(parents=True, exist_ok=True)
        
        image_path = base_dir / "bing.jpg"
        meta_path = base_dir / "meta.json"
        thumb_path = base_dir / "thumb.jpg"
        story_path = base_dir / "story.md"
        
        # 1. 下载和处理基本文件 (如果不存在)
        if not image_path.exists():
            image_url = BING_BASE + img["url"]
            print(f"📥 正在下载 {date_str}: {img.get('title')}")
            fetch_bing_wallpaper.download_image(image_url, image_path)
            fetch_bing_wallpaper.generate_thumbnail(image_path, thumb_path)
            count += 1
        
        # 2. 检查并生成 AI 故事
        has_story = story_path.exists()
        if not has_story:
            story_content = fetch_bing_wallpaper.generate_story(
                img.get("title"), 
                img.get("copyright"),
                image_path
            )
            if story_content:
                story_path.write_text(story_content, encoding="utf-8")
                print(f"📖 已生成故事: {date_str}")
                has_story = True
                story_count += 1

        # 3. 始终更新 meta.json 以确保 has_story 字段准确
        meta_info = {
            "date": date_str,
            "title": img.get("title"),
            "copyright": img.get("copyright"),
            "image_url": BING_BASE + img["url"],
            "has_story": has_story
        }
        meta_path.write_text(json.dumps(meta_info, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✅ 批量处理完成：新增图片 {count} 张，补全故事 {story_count} 篇。")
    
    # 更新索引
    print("🔄 正在更新 README 和 Gallery...")
    update_readme()
    update_gallery()

if __name__ == "__main__":
    batch_fetch("2025-12")
