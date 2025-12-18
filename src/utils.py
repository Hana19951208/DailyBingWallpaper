#!/usr/bin/env python3
"""
企业微信群机器人推送工具
"""

import base64
import hashlib
import requests


def send_image_to_wecom(webhook_url: str, image_path: str):
    """
    发送图片到企业微信群机器人
    
    注意：企业微信群机器人不支持直接发送图片 URL，
    必须将图片转换为 base64 编码后发送。
    """
    with open(image_path, "rb") as f:
        image_data = f.read()
        image_base64 = base64.b64encode(image_data).decode("utf-8")
        image_md5 = hashlib.md5(image_data).hexdigest()

    payload = {
        "msgtype": "image",
        "image": {
            "base64": image_base64,
            "md5": image_md5
        }
    }

    resp = requests.post(webhook_url, json=payload, timeout=10)
    resp.raise_for_status()
    
    result = resp.json()
    if result.get("errcode") != 0:
        raise Exception(f"WeChat push failed: {result.get('errmsg')}")


def send_markdown_to_wecom(webhook_url: str, meta: dict):
    """
    发送 Markdown 消息到企业微信群机器人
    """
    title = meta.get("title", "")
    copyright_info = meta.get("copyright", "")
    date = meta.get("date", "")

    content = f"""### 🖼 今日必应壁纸 · {date}

**{title}**

> {copyright_info}

📦 已自动归档至 [GitHub 仓库](https://github.com)
🔁 每日 08:00 自动更新"""

    payload = {
        "msgtype": "markdown",
        "markdown": {
            "content": content
        }
    }

    resp = requests.post(webhook_url, json=payload, timeout=10)
    resp.raise_for_status()
    
    result = resp.json()
    if result.get("errcode") != 0:
        raise Exception(f"WeChat push failed: {result.get('errmsg')}")


def send_story_to_wecom(webhook_url: str, meta: dict, story_content: str):
    """
    推送壁纸故事到企业微信（Markdown 格式）
    企业微信 Markdown 消息限制 2048 字节，超出则截断
    """
    try:
        title = meta.get("title", "每日壁纸")
        date = meta.get("date", "")
        
        # 构建 Markdown 内容
        # 移除图片引用（企业微信 Markdown 不支持图片）
        story_text = story_content.replace(f"![{title}](bing.jpg)", "").strip()
        
        # 限制长度（企业微信限制 2048 字节）
        max_length = 1800  # 留一些余量给标题和格式
        if len(story_text.encode('utf-8')) > max_length:
            # 截断并添加省略号
            while len(story_text.encode('utf-8')) > max_length:
                story_text = story_text[:-10]
            story_text += "\n\n...\n\n> 查看完整故事请访问 GitHub 仓库"
        
        markdown_text = f"# 📖 {title}\n\n**日期**: {date}\n\n---\n\n{story_text}"
        
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "content": markdown_text
            }
        }
        
        resp = requests.post(webhook_url, json=payload, timeout=10)
        resp.raise_for_status()
        result = resp.json()
        
        if result.get("errcode") != 0:
            print(f"[WARN] 企业微信故事推送返回错误: {result.get('errmsg')}")
    except Exception as e:
        print(f"[ERROR] 企业微信故事推送失败: {e}")
