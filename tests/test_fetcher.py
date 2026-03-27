from __future__ import annotations

from nonebot_plugin_ai_news.fetcher import NewsItem, _clean_html


def test_clean_html():
    assert _clean_html("<p>Hello <b>world</b></p>") == "Hello world"
    assert _clean_html("&amp; &lt;tag&gt;") == "& <tag>"


def test_news_item_format():
    item = NewsItem(
        title="GPT-5 Released",
        url="https://example.com/gpt5",
        source="OpenAI",
        summary="A new model that changes everything.",
    )
    text = item.format_text()
    assert "GPT-5 Released" in text
    assert "https://example.com/gpt5" in text
    assert "OpenAI" in text
