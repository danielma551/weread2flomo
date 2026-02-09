<div align="center">
    <img src="./assets/images/flomo.png" alt="WeRead2Flomo Logo" width="80"/>
    <h1>WeRead2Flomo</h1>
    <p><strong>同步微信读书划线到 Flomo | AI 智能摘要 | Telegram 通知 | GitHub Actions 自动化</strong></p>
</div>

<p align="center">
    <a href="https://github.com/blessonism/weread2flomo/stargazers"><img src="https://img.shields.io/github/stars/blessonism/weread2flomo?style=social" alt="GitHub stars"/></a>
    <a href="https://github.com/blessonism/weread2flomo/blob/main/LICENSE"><img src="https://img.shields.io/github/license/blessonism/weread2flomo" alt="License"/></a>
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python"/></a>
    <a href="https://github.com/blessonism/weread2flomo/issues"><img src="https://img.shields.io/github/issues/blessonism/weread2flomo" alt="Issues"/></a>
    <a href="https://weread2flomo.sukisq.me"><img src="https://img.shields.io/badge/docs-weread2flomo.sukisq.me-blue.svg" alt="Docs"/></a>
</p>

<details>
<summary><strong>📸 点击查看运行效果</strong></summary>
<br/>
<div align="center">
  <img src="./assets/images/screenshot_1.jpg" alt="功能演示" width="800"/>
</div>
</details>

---

## 功能一览

| 功能 | 说明 |
|------|------|
| 📝 **自动同步** | 定时同步微信读书划线到 Flomo，增量去重 |
| 🤖 **AI 智能摘要** | 为长划线自动生成一句话概述 |
| 🏷️ **AI 智能标签** | 自动提取主题，生成精准标签 |
| 🎨 **多模板系统** | 简洁/标准/详细三种模板 + 自定义 |
| 📬 **Telegram 通知** | 同步完成后推送详细报告 |
| 🍪 **Cookie Cloud** | 自动同步浏览器 Cookie，无需手动更新 |
| ⏱️ **GitHub Actions** | 每天自动运行，无需本地部署 |

> 📖 功能详细说明和使用场景：[FEATURES.md](docs/FEATURES.md)

---

## 🚀 快速开始

### 方式一：GitHub Actions 自动化（推荐）

> 无需本地环境，Fork 后配置即用，每天自动同步。

**1. Fork 本仓库**

**2. 配置 Secrets**

进入你 Fork 后的仓库 → `Settings` → `Secrets and variables` → `Actions`，添加：

| Secret | 必填 | 说明 |
|--------|------|------|
| `CC_URL` | 是 | Cookie Cloud 服务器地址 |
| `CC_ID` | 是 | Cookie Cloud UUID |
| `CC_PASSWORD` | 是 | Cookie Cloud 密码 |
| `FLOMO_API` | 是 | Flomo API 地址 |
| `AI_API_KEY` | 否 | AI API Key（开启 AI 摘要/标签） |
| `TELEGRAM_BOT_TOKEN` | 否 | Telegram Bot Token（开启通知） |
| `TELEGRAM_CHAT_ID` | 否 | Telegram Chat ID（开启通知） |

> 不使用 Cookie Cloud？也可以用 `WEREAD_COOKIE` 代替前三项，详见 [Cookie 配置指南](docs/COOKIE_GUIDE.md)

**3. 启用 Actions**

进入 `Actions` 标签页 → 启用工作流 → 完成！

每天北京时间 08:00 自动同步，也可手动触发：`Actions` → `Run workflow`

> 📖 详细教程：[GitHub Actions 配置指南](docs/GITHUB_ACTIONS_GUIDE.md)

### 方式二：本地运行

```bash
git clone https://github.com/blessonism/weread2flomo.git
cd weread2flomo
pip install -r requirements.txt
cp .env.example .env  # 编辑 .env 填入配置
python sync.py
```

> 📖 完整本地部署教程：[快速开始指南](docs/QUICKSTART_CN.md)

---

## ⚙️ 配置速查

配置优先级：**环境变量（.env）> config.yaml > 默认值**

<details>
<summary><strong>必填配置</strong></summary>

| 配置项 | 环境变量 | 说明 |
|--------|----------|------|
| 微信读书认证 | `CC_URL` + `CC_ID` + `CC_PASSWORD`<br/>或 `WEREAD_COOKIE` | Cookie Cloud（推荐）或手动 Cookie |
| Flomo API | `FLOMO_API` | Flomo 官方 API 地址 |

</details>

<details>
<summary><strong>AI 功能（可选）</strong></summary>

| 配置项 | 环境变量 | 说明 |
|--------|----------|------|
| API 密钥 | `AI_API_KEY` | OpenAI 格式的 API Key |
| API 地址 | `AI_API_BASE` | 支持所有 OpenAI 兼容服务 |
| 模型名称 | `AI_MODEL` | 如 `gpt-5`、`claude-4.5-sonnet` 等 |
| 启用摘要 | - | `config.yaml` 中 `ai.enable_summary: true` |
| 启用标签 | - | `config.yaml` 中 `tags.enable_ai_tags: true` |

</details>

<details>
<summary><strong>Telegram 通知（可选）</strong></summary>

每次同步完成后，自动推送报告到 Telegram，包含同步数量、书籍详情、AI 统计等。

| 配置项 | 环境变量 | 说明 |
|--------|----------|------|
| Bot Token | `TELEGRAM_BOT_TOKEN` | 通过 [@BotFather](https://t.me/BotFather) 创建 Bot 获取 |
| Chat ID | `TELEGRAM_CHAT_ID` | 通过 [@userinfobot](https://t.me/userinfobot) 获取 |
| 启用开关 | - | `config.yaml` 中 `notification.telegram.enabled: true` |
| 自定义 API | `TELEGRAM_API_BASE` | 默认 `https://api.telegram.org`，支持反代 |

</details>

<details>
<summary><strong>同步配置（可选）</strong></summary>

| 配置项 | 环境变量 | 默认值 | 说明 |
|--------|----------|--------|------|
| 时间限制 | `SYNC_DAYS_LIMIT` | 100 | 只同步最近 N 天的划线 |
| 最大数量 | `SYNC_MAX_HIGHLIGHTS` | 50 | 每次最多同步 N 条 |
| 同步笔记 | `SYNC_REVIEWS` | true | 是否同步笔记 |

</details>

> 📖 完整配置文档：[CONFIG_GUIDE.md](docs/CONFIG_GUIDE.md)

---

## ❓ 常见问题

<details>
<summary><strong>Cookie 怎么获取？会过期吗？</strong></summary>

推荐使用 **Cookie Cloud** 自动同步，无需手动操作。详见 [Cookie Cloud 配置指南](docs/COOKIE_CLOUD_GUIDE.md)。

手动获取：浏览器登录 weread.qq.com → F12 开发者工具 → Application → Cookies。有效期较短，需定期更新。

</details>

<details>
<summary><strong>GitHub Actions 没有运行 / 运行失败？</strong></summary>

- 仓库 60 天无活动会被 GitHub 自动禁用 → `Actions` 页面重新启用
- 检查 `Settings` → `Actions` → `Workflow permissions` 设为 `Read and write permissions`
- 检查所有必填 Secrets 是否配置正确
- 定时任务可能有 5 分钟 ~ 2 小时延迟，属正常现象

</details>

<details>
<summary><strong>有的划线没有同步？</strong></summary>

1. Flomo API 每日限制 100 次
2. 检查 `days_limit` 时间范围设置
3. 已同步过的不会重复（查看 `synced_bookmarks.json`）
4. Cookie 可能已过期

</details>

<details>
<summary><strong>Telegram 通知收不到？</strong></summary>

1. 检查 `TELEGRAM_BOT_TOKEN` 和 `TELEGRAM_CHAT_ID` 是否正确
2. `config.yaml` 中 `notification.telegram.enabled` 需为 `true`
3. 首次使用需先向 Bot 发送一条消息激活对话
4. 网络问题可通过 `TELEGRAM_API_BASE` 配置反代

</details>

> 📖 更多问题：[完整 FAQ](docs/FEATURES.md)

---

## 📖 了解更多

| 文档 | 说明 |
|------|------|
| [功能特性详解](docs/FEATURES.md) | 模板示例、AI 功能、使用场景、高级用法 |
| [完整配置指南](docs/CONFIG_GUIDE.md) | 所有配置项详细说明 |
| [Cookie Cloud 指南](docs/COOKIE_CLOUD_GUIDE.md) | Cookie Cloud 安装和配置教程 |
| [GitHub Actions 指南](docs/GITHUB_ACTIONS_GUIDE.md) | 自动化部署详细步骤、Cron 表达式 |
| [Secrets 配置指南](docs/SECRETS_GUIDE.md) | GitHub Secrets 配置方法 |
| [快速开始（中文）](docs/QUICKSTART_CN.md) | 完整的本地部署教程 |

---

## 🙏 致谢

- [weread2notion](https://github.com/malinkang/weread2notion) - 微信读书同步方案参考
- [Flomo](https://flomoapp.com/) - 优秀的笔记工具
- [Cookie Cloud](https://github.com/easychen/CookieCloud) - Cookie 同步方案

---

## 👥 贡献

欢迎贡献代码、报告问题或提出建议！

- 🐛 [报告 Bug](https://github.com/blessonism/weread2flomo/issues) · 💡 [功能建议](https://github.com/blessonism/weread2flomo/issues) · 🔧 [提交 PR](https://github.com/blessonism/weread2flomo/pulls)

<p align="center">
  <a href="https://github.com/blessonism/weread2flomo/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=blessonism/weread2flomo&max=20" alt="Contributors" />
  </a>
</p>

---

## 📄 许可证

[MIT License](LICENSE)

---

<p align="center">
  <a href="https://www.star-history.com/#blessonism/weread2flomo&Date" target="_blank">
    <img src="https://api.star-history.com/svg?repos=blessonism/weread2flomo&type=Date" alt="GitHub Stars Trend" width="500">
  </a>
</p>

<div align="center">

**⭐ 如果这个项目对你有帮助，请给个 Star 支持一下！**

</div>
