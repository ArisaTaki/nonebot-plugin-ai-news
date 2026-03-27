from __future__ import annotations

from pathlib import Path

import nonebot_plugin_localstore as localstore

from .store import NewsStore


def _get_store_path() -> Path:
    return localstore.get_data_file("nonebot_plugin_ai_news", "store.json")


store = NewsStore(_get_store_path())
