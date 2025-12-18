#!/usr/bin/env python3
"""
配置加载器 - 管理壁纸源配置
"""

import yaml
from pathlib import Path
from typing import List, Dict, Any


def load_sources_config() -> Dict[str, Any]:
    """加载壁纸源配置"""
    config_path = Path("config/sources.yaml")
    if config_path.exists():
        return yaml.safe_load(config_path.read_text(encoding="utf-8"))
    
    # 默认配置
    return {
        "sources": [
            {
                "name": "bing",
                "display_name": "Bing 🔍",
                "enabled": True
            }
        ],
        "display": {
            "max_items_per_source": 10,
            "columns": "auto"
        }
    }


def get_enabled_sources() -> List[Dict[str, Any]]:
    """获取所有启用的壁纸源"""
    config = load_sources_config()
    return [s for s in config.get("sources", []) if s.get("enabled", False)]


def get_display_config() -> Dict[str, Any]:
    """获取显示配置"""
    config = load_sources_config()
    return config.get("display", {"max_items_per_source": 10, "columns": "auto"})


if __name__ == "__main__":
    print("Enabled sources:", get_enabled_sources())
    print("Display config:", get_display_config())
