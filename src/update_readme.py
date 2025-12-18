#!/usr/bin/env python3
"""
更新 README.md 中的壁纸索引
使用更精美的 HTML 表格布局 (自适应 1 或 2 列)
"""

import re
import json
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

    if not dates:
        return

    # 如果只有一张图，使用一行展示一个。如果有两张或更多，每行展示两个。
    columns = 2 if len(dates) > 1 else 1
    
    html_output = ['<table width="100%">']
    
    # 将日期按 columns 分组
    chunks = [dates[i:i + columns] for i in range(0, len(dates), columns)]
    
    for chunk in chunks:
        html_output.append('<tr>')
        for d in chunk:
            thumb = f"wallpapers/{d}/thumb.jpg"
            img_url = f"wallpapers/{d}/bing.jpg"
            
            # 尝试读取元数据获取标题
            title = d
            meta_path = base / d / "meta.json"
            if meta_path.exists():
                try:
                    meta = json.loads(meta_path.read_text(encoding="utf-8"))
                    title = meta.get("title", d)
                except:
                    pass
            
            # 标题链接：如果有 story.md 则链接到它，否则无链接
            story_path = base / d / "story.md"
            title_display = f'<b>{d}</b><br /><small>{title}</small>'
            if story_path.exists():
                # 使用 ../wallpapers/.. 相对路径可能在预览时不工作，但在 GitHub 仓库视图中通常是 OK 的
                # 为了兼容性，在 README 中我们通常相对于 README 所在位置引用，即 wallpapers/2025-xx-xx/story.md
                # 如果用户反映不跳转，可能是因为 GitHub 不允许非 markdown 扩展名的跳转？不，story.md 是 markdown。
                # 还有一种可能是 HTML 里面的 <a> 标签行为。
                # 尝试使用 GitHub 绝对路径风格？不，通用性差。
                # 重新确认逻辑，确保路径正确。
                title_link = f"wallpapers/{d}/story.md"
                title_display = f'<a href="{title_link}"><b>{d}</b><br /><small>{title} 📖</small></a>'
            
            cell_width = "100%" if columns == 1 else "50%"
            # 关键：不要在前缀留空格，否则 GitHub 会认为这是代码块
            cell_content = f'<td width="{cell_width}" align="center" valign="top"><a href="{img_url}"><img src="{thumb}" width="100%" style="border-radius:10px;"></a><br />{title_display}</td>'
            html_output.append(cell_content)
        
        if columns == 2 and len(chunk) < 2:
            html_output.append('<td width="50%"></td>')
            
        html_output.append('</tr>')
    
    html_output.append('</table>')

    index_block = "\n".join(html_output)

    # 读取 README
    readme_content = readme_path.read_text(encoding="utf-8")

    # 使用正则替换锚点之间的内容
    pattern = r"(<!-- WALLPAPER_INDEX_START -->)[\s\S]*?(<!-- WALLPAPER_INDEX_END -->)"
    replacement = f"\\1\n{index_block}\n\\2"

    new_content = re.sub(pattern, replacement, readme_content)

    readme_path.write_text(new_content, encoding="utf-8")


if __name__ == "__main__":
    update_readme()
    print("[OK] README.md 已更新 (精美表格模式)")
