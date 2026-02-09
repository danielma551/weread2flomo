# 🚀 5分钟快速开始

本指南帮助你在 5 分钟内完成配置并开始使用 WeRead2Flomo。

## 步骤 1：安装项目（1分钟）

```bash
# 克隆项目
git clone https://github.com/blessonism/weread2flomo.git
cd weread2flomo

# 安装依赖
pip install -r requirements.txt
```

## 步骤 2：获取必要的配置（2分钟）

### 2.1 获取 Flomo API

1. 访问 [Flomo 网页版](https://flomoapp.com/)
2. 点击右上角头像 → API
3. 复制 API 地址（格式：`https://flomoapp.com/iwh/xxxxx/`）

### 2.2 获取微信读书 Cookie

**方式 1：快速方式（手动 Cookie）**

1. 浏览器访问 [微信读书网页版](https://weread.qq.com/)
2. 使用微信扫码登录
3. 按 `F12` 打开开发者工具
4. 切换到 `Application` → `Cookies` → `weread.qq.com`
5. 复制所有 Cookie 值

**方式 2：推荐方式（Cookie Cloud，自动更新）**

参考：[Cookie Cloud 配置指南](COOKIE_CLOUD_GUIDE.md)

## 步骤 3：配置环境变量（1分钟）

创建 `.env` 文件：

```bash
# Flomo API（必需）
FLOMO_API="https://flomoapp.com/iwh/你的API密钥/"

# 微信读书 Cookie（必需）
WEREAD_COOKIE="你的Cookie"

# 或使用 Cookie Cloud（推荐）
# CC_URL="https://cc.chenge.ink"
# CC_ID="你的UUID"
# CC_PASSWORD="你的密码"

# AI 功能（可选）
# AI_API_KEY="你的AI API Key"

# Telegram 通知（可选）
# TELEGRAM_BOT_TOKEN="你的Bot Token"
# TELEGRAM_CHAT_ID="你的Chat ID"
```

## 步骤 4：测试运行（1分钟）

```bash
# 运行同步
python sync.py
```

## 步骤 5：查看结果

打开 Flomo，你应该能看到同步的读书笔记了！

## 🎉 完成！

现在你可以：

1. **自动化同步** - 设置 [GitHub Actions](GITHUB_ACTIONS_GUIDE.md) 每天自动同步
2. **启用 AI 功能** - 配置 AI API 获得智能摘要和标签
3. **启用 Telegram 通知** - 同步完成后自动推送报告
4. **自定义模板** - 在 `config.yaml` 中调整模板
5. **调整配置** - 根据需要修改同步规则

## 📖 下一步

- [完整配置指南](CONFIG_GUIDE.md)
- [Cookie Cloud 配置](COOKIE_CLOUD_GUIDE.md)
- [GitHub Actions 自动化](GITHUB_ACTIONS_GUIDE.md)

## ❓ 遇到问题？

1. 查看 [常见问题](../README.md#-常见问题)
2. 提交 [Issue](https://github.com/blessonism/weread2flomo/issues)
3. 查看完整文档：[docs/README.md](README.md)

---

**祝你使用愉快！** 🎊

