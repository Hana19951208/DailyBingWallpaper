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
