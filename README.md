# nonebot-plugin-ai-news

AI 前沿资讯定时推送插件，自动从 RSS 源收集 AI 领域新闻（模型、工具、新技术、行业动态），定时推送到订阅的 QQ 群。

## 安装

```bash
nb plugin install nonebot-plugin-ai-news
```

或使用 `pip` 安装：

```bash
pip install nonebot-plugin-ai-news
```

然后在 NoneBot 中加载插件：

```toml
[tool.nonebot]
plugins = ["nonebot_plugin_ai_news"]
```

## 配置

在 `.env` 文件中可选配置：

```env
# 推送间隔（分钟），默认 60
AI_NEWS_INTERVAL=60

# 每次推送最大条数，默认 5
AI_NEWS_MAX_ITEMS=5

# 自定义 RSS 源（JSON 数组），留空使用内置源
# AI_NEWS_RSS_URLS='["https://your-custom-feed.com/rss"]'
```

### 内置 RSS 源

| 源 | 地址 |
|---|---|
| Hugging Face Blog | `https://huggingface.co/blog/feed.xml` |
| 机器之心 | `https://www.jiqizhixin.com/rss` |
| AI 前线（InfoQ） | `https://ai.infoq.cn/feed` |

## 指令

| 指令 | 权限 | 说明 |
|---|---|---|
| `AI订阅` | 群管理员 | 当前群订阅 AI 新闻推送 |
| `取消AI订阅` | 群管理员 | 取消当前群订阅 |
| `AI新闻` | 所有人 | 立即获取最新 AI 新闻 |
| `AI订阅状态` | 所有人 | 查看当前群订阅状态 |
