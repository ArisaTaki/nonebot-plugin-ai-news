from __future__ import annotations

from typing import List, Optional

from nonebot import get_driver
from pydantic import BaseModel


DEFAULT_RSS_URLS: list[str] = [
    "https://huggingface.co/blog/feed.xml",
    "https://www.jiqizhixin.com/rss",
]


class Config(BaseModel):
    ai_news_interval: int = 60
    ai_news_max_items: int = 5
    ai_news_rss_urls: Optional[List[str]] = None

    @property
    def rss_urls(self) -> list[str]:
        return self.ai_news_rss_urls or DEFAULT_RSS_URLS


_config: Config | None = None


def get_config() -> Config:
    global _config
    if _config is None:``
        _config = Config(**get_driver().config.model_dump())
    return _config
