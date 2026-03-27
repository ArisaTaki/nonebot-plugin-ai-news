from nonebot import get_driver, require
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="AI News",
    description="AI 前沿资讯定时推送插件，自动收集 AI 领域新闻并推送到订阅群聊。",
    usage=(
        "AI订阅 —— 订阅 AI 新闻推送（管理员）\n"
        "取消AI订阅 —— 取消订阅（管理员）\n"
        "AI新闻 —— 立即获取最新 AI 资讯\n"
        "AI订阅状态 —— 查看当前群订阅状态"
    ),
    type="application",
    homepage="https://github.com/ArisaTaki/nonebot-plugin-ai-news",
    config=Config,
    supported_adapters={"~onebot.v11"},
)

try:
    get_driver()
except ValueError:
    pass
else:
    require("nonebot_plugin_localstore")
    require("nonebot_plugin_apscheduler")

    from . import commands as commands  # noqa: F401
    from .scheduler import setup_scheduler

    get_driver().on_startup(setup_scheduler)

__all__ = ["__plugin_meta__"]
