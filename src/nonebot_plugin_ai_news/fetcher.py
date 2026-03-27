from __future__ import annotations

import html
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from time import mktime
from typing import Optional

import feedparser
import httpx
from nonebot import logger

from .config import get_config

_TAG_RE = re.compile(r"<[^>]+>")


@dataclass
class NewsItem:
    title: str
    url: str
    source: str
    summary: str
    published: Optional[datetime] = None

    def format_text(self) -> str:
        parts = [f"📰 {self.title}"]
        if self.summary:
            parts.append(self.summary[:120] + ("..." if len(self.summary) > 120 else ""))
        parts.append(f"🔗 {self.url}")
        parts.append(f"📡 来源：{self.source}")
        return "\n".join(parts)


def _clean_html(raw: str) -> str:
    text = _TAG_RE.sub("", raw)
    return html.unescape(text).strip()


def _parse_source_name(url: str) -> str:
    if "huggingface" in url:
        return "Hugging Face"
    if "jiqizhixin" in url:
        return "机器之心"
    if "infoq" in url:
        return "AI 前线"
    if "openai" in url:
        return "OpenAI"
    if "google" in url:
        return "Google AI"
    return url.split("/")[2] if "/" in url else url


async def _fetch_feed(client: httpx.AsyncClient, url: str) -> list[NewsItem]:
    items: list[NewsItem] = []
    try:
        resp = await client.get(url, follow_redirects=True)
        resp.raise_for_status()
        feed = feedparser.parse(resp.text)
        source = _parse_source_name(url)

        for entry in feed.entries[:20]:
            title = entry.get("title", "").strip()
            link = entry.get("link", "").strip()
            if not title or not link:
                continue

            summary_raw = entry.get("summary", "") or entry.get("description", "")
            summary = _clean_html(summary_raw)

            published = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                try:
                    published = datetime.fromtimestamp(
                        mktime(entry.published_parsed), tz=timezone.utc
                    )
                except Exception:
                    pass

            items.append(
                NewsItem(
                    title=title,
                    url=link,
                    source=source,
                    summary=summary,
                    published=published,
                )
            )
    except Exception as e:
        logger.warning("[ai_news] failed to fetch %s: %s", url, e)

    return items


async def fetch_all_news() -> list[NewsItem]:
    config = get_config()
    all_items: list[NewsItem] = []

    async with httpx.AsyncClient(timeout=15.0) as client:
        for url in config.rss_urls:
            items = await _fetch_feed(client, url)
            all_items.extend(items)

    all_items.sort(
        key=lambda x: x.published or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )
    return all_items
