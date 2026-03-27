from __future__ import annotations

from pathlib import Path

import pytest

from nonebot_plugin_ai_news.store import NewsStore


@pytest.mark.asyncio
async def test_subscribe_and_unsubscribe(tmp_path: Path):
    store = NewsStore(tmp_path / "store.json")
    assert await store.subscribe(12345) is True
    assert await store.subscribe(12345) is False
    assert store.is_subscribed(12345) is True

    reloaded = NewsStore(tmp_path / "store.json")
    assert reloaded.is_subscribed(12345) is True

    assert await reloaded.unsubscribe(12345) is True
    assert reloaded.is_subscribed(12345) is False


@pytest.mark.asyncio
async def test_mark_pushed(tmp_path: Path):
    store = NewsStore(tmp_path / "store.json")
    assert store.is_pushed("https://example.com/1") is False

    await store.mark_pushed(["https://example.com/1", "https://example.com/2"])
    assert store.is_pushed("https://example.com/1") is True
    assert store.is_pushed("https://example.com/2") is True

    reloaded = NewsStore(tmp_path / "store.json")
    assert reloaded.is_pushed("https://example.com/1") is True
