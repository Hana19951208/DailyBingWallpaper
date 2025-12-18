#!/usr/bin/env python3
"""
更新 README.md 中的壁纸索引
"""

import re
from pathlib import Path


def update_readme():
    """更新 README.md 中 WALLPAPER_INDEX 锚点区域的内容"""
    base = Path("wallpapers")
    readme_path = Path("README.md")

    # 获取所有日期目录，按日期倒序排列
    dates = sorted(
        [p.name for p in base.iterdir() if p.is_dir()],
        reverse=True
    )

    # 生成索引内容
    lines = []
    for d in dates:
        thumb = f"wallpapers/{d}/thumb.jpg"
        lines.append(f"- **{d}**  \n  ![]({thumb})")

    index_block = "\n".join(lines)

    # 读取 README
    readme_content = readme_path.read_text(encoding="utf-8")

    # 使用正则替换锚点之间的内容（包括已有内容）
    pattern = r"(<!-- WALLPAPER_INDEX_START -->)[\s\S]*?(<!-- WALLPAPER_INDEX_END -->)"
    replacement = f"\\1\n{index_block}\n\\2"

    new_content = re.sub(pattern, replacement, readme_content)

    readme_path.write_text(new_content, encoding="utf-8")


if __name__ == "__main__":
    update_readme()
    print("[OK] README.md 已更新")
