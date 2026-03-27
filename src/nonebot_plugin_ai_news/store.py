from __future__ import annotations

import asyncio
import json
from pathlib import Path

from nonebot import logger


class NewsStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.subscribed_groups: list[int] = []
        self.pushed_urls: list[str] = []
        self.storage_available = True
        self.load()

    def load(self) -> None:
        if not self.path.exists():
            logger.info("[ai_news] no data file, start fresh")
            return

        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            self.subscribed_groups = raw.get("subscribed_groups", [])
            self.pushed_urls = raw.get("pushed_urls", [])
            logger.info(
                "[ai_news] loaded %d groups, %d pushed records",
                len(self.subscribed_groups),
                len(self.pushed_urls),
            )
        except Exception as e:
            logger.error("[ai_news] failed to load store: %s", e)
            self.subscribed_groups = []
            self.pushed_urls = []

    async def save(self) -> None:
        try:
            payload = json.dumps(
                {
                    "subscribed_groups": self.subscribed_groups,
                    "pushed_urls": self.pushed_urls[-500:],
                },
                ensure_ascii=False,
                indent=2,
            )
            await asyncio.to_thread(
                self.path.write_text, payload, encoding="utf-8"
            )
        except Exception as e:
            logger.error("[ai_news] failed to save store: %s", e)

    async def subscribe(self, group_id: int) -> bool:
        if group_id in self.subscribed_groups:
            return False
        self.subscribed_groups.append(group_id)
        await self.save()
        return True

    async def unsubscribe(self, group_id: int) -> bool:
        if group_id not in self.subscribed_groups:
            return False
        self.subscribed_groups.remove(group_id)
        await self.save()
        return True

    def is_subscribed(self, group_id: int) -> bool:
        return group_id in self.subscribed_groups

    def is_pushed(self, url: str) -> bool:
        return url in self.pushed_urls

    async def mark_pushed(self, urls: list[str]) -> None:
        self.pushed_urls.extend(urls)
        if len(self.pushed_urls) > 500:
            self.pushed_urls = self.pushed_urls[-500:]
        await self.save()
