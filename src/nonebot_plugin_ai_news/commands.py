from __future__ import annotations

from nonebot import on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.permission import SUPERUSER

from .config import get_config
from .fetcher import fetch_all_news
from .runtime import store

ADMIN_PERMISSION = SUPERUSER | GROUP_ADMIN | GROUP_OWNER

sub_cmd = on_command(
    "AI订阅",
    permission=ADMIN_PERMISSION,
    priority=5,
    block=True,
)


@sub_cmd.handle()
async def _handle_subscribe(event: GroupMessageEvent):
    ok = await store.subscribe(event.group_id)
    if ok:
        await sub_cmd.finish("已订阅 AI 新闻推送，将定时推送最新 AI 资讯到本群")
    else:
        await sub_cmd.finish("本群已订阅，无需重复操作")


unsub_cmd = on_command(
    "取消AI订阅",
    permission=ADMIN_PERMISSION,
    priority=5,
    block=True,
)


@unsub_cmd.handle()
async def _handle_unsubscribe(event: GroupMessageEvent):
    ok = await store.unsubscribe(event.group_id)
    if ok:
        await unsub_cmd.finish("已取消 AI 新闻推送")
    else:
        await unsub_cmd.finish("本群未订阅")


status_cmd = on_command(
    "AI订阅状态",
    priority=5,
    block=True,
)


@status_cmd.handle()
async def _handle_status(event: GroupMessageEvent):
    config = get_config()
    if store.is_subscribed(event.group_id):
        await status_cmd.finish(
            f"本群已订阅 AI 新闻推送\n"
            f"推送间隔：{config.ai_news_interval} 分钟\n"
            f"每次最多：{config.ai_news_max_items} 条\n"
            f"RSS 源数量：{len(config.rss_urls)}"
        )
    else:
        await status_cmd.finish("本群未订阅 AI 新闻推送，管理员发送「AI订阅」开启")


news_cmd = on_command(
    "AI新闻",
    priority=5,
    block=True,
)


@news_cmd.handle()
async def _handle_news():
    config = get_config()
    await news_cmd.send("正在获取最新 AI 资讯...")

    items = await fetch_all_news()
    if not items:
        await news_cmd.finish("暂未获取到新闻，请稍后重试")

    messages: list[str] = []
    for item in items[: config.ai_news_max_items]:
        messages.append(item.format_text())

    header = f"🤖 最新 AI 资讯（共 {len(messages)} 条）\n" + "=" * 20
    await news_cmd.finish(header + "\n\n" + "\n\n".join(messages))
