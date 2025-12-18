#!/usr/bin/env python3
"""
每日必应壁纸自动归档脚本
- 下载必应每日壁纸
- 生成缩略图
- 更新 README 索引
- 更新 Gallery 页面
- 推送企业微信
"""

import os
import json
import requests
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image

from src.utils import send_image_to_wecom, send_markdown_to_wecom
from src.update_readme import update_readme
from src.update_gallery import update_gallery


BING_API = "https://www.bing.com/HPImageArchive.aspx"
BING_BASE = "https://www.bing.com"
THUMB_SIZE = (400, 225)  # 16:9 缩略图


def load_env():
    """手动从 .env 文件加载环境变量 (为了避免增加 python-dotenv 依赖)"""
    env_path = Path(".env")
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip()


def get_today_str():
    """获取今日日期字符串 (UTC)"""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def fetch_bing_metadata():
    """获取必应每日壁纸元数据"""
    params = {
        "format": "js",
        "idx": 0,
        "n": 1,
        "mkt": "zh-CN"
    }
    resp = requests.get(BING_API, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return data["images"][0]


def download_image(url: str, save_path: Path):
    """下载图片到指定路径"""
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    save_path.write_bytes(r.content)


def generate_thumbnail(image_path: Path, thumb_path: Path):
    """生成缩略图"""
    with Image.open(image_path) as img:
        img.thumbnail(THUMB_SIZE, Image.Resampling.LANCZOS)
        img.save(thumb_path, "JPEG", quality=85)


def push_to_wecom(webhook_url: str, image_path: Path, meta: dict):
    """推送图片和消息到企业微信"""
    try:
        # 先发送图片
        send_image_to_wecom(webhook_url, str(image_path))
        print("[OK] 企业微信图片推送成功")

        # 再发送 markdown 消息
        send_markdown_to_wecom(webhook_url, meta)
        print("[OK] 企业微信消息推送成功")
    except Exception as e:
        print(f"[WARN] 企业微信推送失败: {e}")


def main():
    load_env()
    today = get_today_str()
    base_dir = Path("wallpapers") / today
    base_dir.mkdir(parents=True, exist_ok=True)

    # 1. 获取元数据
    print(f"[INFO] 正在获取 {today} 的必应壁纸...")
    meta = fetch_bing_metadata()

    # 2. 下载原图
    image_url = BING_BASE + meta["url"]
    image_path = base_dir / "bing.jpg"
    download_image(image_url, image_path)
    print(f"[OK] 壁纸已下载: {image_path}")

    # 3. 生成缩略图
    thumb_path = base_dir / "thumb.jpg"
    generate_thumbnail(image_path, thumb_path)
    print(f"[OK] 缩略图已生成: {thumb_path}")

    # 4. 保存元数据
    meta_path = base_dir / "meta.json"
    meta_info = {
        "date": today,
        "title": meta.get("title"),
        "copyright": meta.get("copyright"),
        "image_url": image_url
    }
    meta_path.write_text(
        json.dumps(meta_info, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"[OK] 元数据已保存: {meta_path}")

    # 5. 更新 README
    update_readme()
    print("[OK] README.md 已更新")

    # 6. 更新 Gallery
    update_gallery()
    print("[OK] docs/index.html 已更新")

    # 7. 推送企业微信
    webhook_url = os.environ.get("WEWORK_WEBHOOK")
    if webhook_url:
        push_to_wecom(webhook_url, image_path, meta_info)
    else:
        print("[INFO] WEWORK_WEBHOOK 未配置，跳过企业微信推送")

    print(f"\n✅ 完成！壁纸已归档至 {base_dir}")


if __name__ == "__main__":
    main()
