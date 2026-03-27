from __future__ import annotations

from nonebot import get_bots, logger
from nonebot_plugin_apscheduler import scheduler

from .config import get_config
from .fetcher import fetch_all_news
from .runtime import store


async def _push_news() -> None:
    if not store.subscribed_groups:
        return

    config = get_config()
    logger.info("[ai_news] scheduled push: fetching news...")

    items = await fetch_all_news()
    new_items = [item for item in items if not store.is_pushed(item.url)]

    if not new_items:
        logger.info("[ai_news] no new items to push")
        return

    to_push = new_items[: config.ai_news_max_items]
    messages: list[str] = []
    for item in to_push:
        messages.append(item.format_text())

    text = (
        f"🤖 AI 资讯推送（{len(messages)} 条新消息）\n"
        + "=" * 20
        + "\n\n"
        + "\n\n".join(messages)
    )

    bots = get_bots()
    if not bots:
        logger.warning("[ai_news] no bots available for push")
        return

    bot = next(iter(bots.values()))

    for group_id in list(store.subscribed_groups):
        try:
            await bot.send_group_msg(group_id=group_id, message=text)
            logger.info("[ai_news] pushed to group %d", group_id)
        except Exception as e:
            logger.warning("[ai_news] failed to push to group %d: %s", group_id, e)

    await store.mark_pushed([item.url for item in to_push])
    logger.info("[ai_news] push complete, marked %d items", len(to_push))


def setup_scheduler() -> None:
    config = get_config()
    scheduler.add_job(
        _push_news,
        "interval",
        minutes=config.ai_news_interval,
        id="ai_news_push",
        replace_existing=True,
    )
    logger.info(
        "[ai_news] scheduler started, interval=%d min", config.ai_news_interval
    )
