#!/usr/bin/env python3
"""
更新 docs/index.html 中的图片画廊
"""

import re
import json
from pathlib import Path


def update_gallery():
    """更新 Gallery 页面，生成图片卡片"""
    base = Path("wallpapers")
    html_path = Path("docs/index.html")

    # 获取所有日期目录，按日期倒序排列
    dates = sorted(
        [p.name for p in base.iterdir() if p.is_dir()],
        reverse=True
    )

    # 生成卡片 HTML
    cards = []
    for d in dates:
        img = f"../wallpapers/{d}/bing.jpg"
        thumb = f"../wallpapers/{d}/thumb.jpg"
        meta_path = base / d / "meta.json"

        # 尝试读取标题
        title = d
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                title = meta.get("title", d)
            except Exception:
                pass

        cards.append(f'''        <div class="card">
            <a href="{img}" target="_blank">
                <img src="{thumb}" alt="{title}" loading="lazy">
            </a>
            <p>{d}</p>
            <span class="title">{title}</span>
        </div>''')

    gallery_content = "\n".join(cards)

    # 读取 HTML
    html_content = html_path.read_text(encoding="utf-8")

    # 使用正则替换 gallery div 内的内容
    pattern = r'(<div class="gallery">)[\s\S]*?(</div>\s*</body>)'
    replacement = f"\\1\n{gallery_content}\n    \\2"

    new_content = re.sub(pattern, replacement, html_content)

    html_path.write_text(new_content, encoding="utf-8")


if __name__ == "__main__":
    update_gallery()
    print("[OK] docs/index.html 已更新")
