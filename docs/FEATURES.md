# ✨ 功能特性详解

WeRead2Flomo 的核心功能和使用场景详细说明。

---

## 🎯 核心功能

### 1. 自动同步

**无需手动操作，自动将微信读书划线同步到 Flomo**

- ✅ 增量同步 - 只同步新内容，自动去重
- ✅ 定时任务 - 支持 GitHub Actions 定时执行
- ✅ 智能限流 - 遵守 API 限制，避免触发风控
- ✅ 错误恢复 - 失败自动重试，不丢失数据

**配置示例：**

```yaml
sync:
  days_limit: 100  # 只同步最近 100 天
  max_highlights_per_sync: 50  # 每次最多 50 条
  sync_reviews: true  # 同步笔记
```

---

### 2. 多模板系统

**三种内置模板 + 自定义，适配不同场景**

#### 📌 简洁模板

适合快速记录，突出划线内容。

```
{highlight_text}

📖 《{book_title}》· {author}

{chapter_info}

{ai_summary_section}{tags}
```

#### 📋 标准模板

均衡展示，包含完整信息。

```
📖 《{book_title}》- {author}

> {highlight_text}

{chapter_info}
🔗 {book_url}

{ai_summary_section}{note_section}{tags}
```

#### 📑 详细模板

深度阅读，记录所有元数据。

```
{highlight_text}

📚 来源：《{book_title}》· {author}
📂 章节：{chapter_info}
📅 时间：{create_time}

{ai_summary_section}{note_section}{tags}
```

#### 🎨 自定义模板

完全自定义，满足个性化需求。

```yaml
templates:
  my_template:
    name: "我的模板"
    format: |
      💡 {highlight_text}
      
      from 《{book_title}》
      
      {tags}
```

---

### 3. AI 智能摘要

**为长划线自动生成一句话概述，提炼核心观点**

#### 工作原理

1. 检测划线长度（默认 ≥ 100 字符）
2. 调用 AI API 分析内容
3. 生成精炼的一句话摘要
4. 添加到 Flomo 笔记中

#### 真实案例

**原文（171字符）：**
> 我们来到一个热带岛屿，在滴滴涕的帮助下，我们消灭了疟疾，在两三年内，拯救了数十万人的生命。这显然是好事。但这数十万被救活的人，以及他们繁衍出的数以百万计的后代，没有衣服穿，没有房子住，无法接受教育，甚至将岛上可供利用的资源全部消耗殆尽。疟疾造成的早夭被消灭了，但营养不良和过度拥挤使得悲惨的生活成为常态，饥饿造成的早亡对更多的人口造成了威胁。

**AI 提炼：**
> ✨ 消灭疟疾本是救命之举，却让岛上数百万新生的人口陷入饥饿、拥挤和无尽的悲惨。

#### 配置

```yaml
ai:
  enable_summary: true
  summary_min_length: 100  # 最小触发长度
  summary_prompt: |
    # 自定义提示词
    请用一句话总结以下内容...
```

---

### 4. AI 智能标签

**自动提取划线主题，生成精准标签**

#### 工作原理

1. 分析划线内容和书籍信息
2. 识别核心主题和关键概念
3. 生成 1-3 个相关标签
4. 与默认标签合并

#### 真实案例

**划线内容：**
> 在金字塔结构中，各层级的重要性一般由上而下逐层递减，顶层的中心思想最为重要，一级思想次之，二级思想再次之...

**AI 生成标签：**
> `#金字塔结构` `#逻辑思维` `#沟通技巧`

**最终标签：**
> `#微信读书/逻辑表达` `#金字塔结构` `#逻辑思维` `#沟通技巧`

#### 配置

```yaml
tags:
  enable_ai_tags: true
  max_ai_tags: 3  # 最多 3 个 AI 标签
  
ai:
  tag_prompt: |
    请为以下书籍划线内容生成1-3个主题标签...
```

---

### 5. 书籍智能分类

**自动识别书籍类型，应用对应的标签和模板**

#### 内置分类

| 分类 | 关键词 | 标签 | 模板 |
|------|--------|------|------|
| 工作类 | 管理、商业、职场 | #工作 #职场 | standard |
| 个人成长 | 思维、心理、习惯 | #个人成长 #自我提升 | standard |
| 文学类 | 小说、散文、诗歌 | #文学 #阅读 | simple |
| 技术类 | 编程、算法、架构 | #技术 #编程 | detailed |

#### 自定义分类

```yaml
book_categories:
  science:
    keywords:
      - "物理"
      - "化学"
      - "生物"
    tags:
      - "#科学"
      - "#知识"
    template: "detailed"
```

---

### 6. Cookie Cloud 支持

**自动同步浏览器 Cookie，告别手动更新**

#### 优势

- ✅ **自动更新** - 无需手动复制 Cookie
- ✅ **长期有效** - Cookie 保活功能保持登录状态
- ✅ **多端同步** - 多个设备共享同一个登录状态
- ✅ **安全加密** - 端对端加密，服务器无法读取
- ✅ **自动容错** - Cookie 失效时自动重新获取

#### 配置

```bash
# .env
CC_URL="https://cc.chenge.ink"
CC_ID="你的UUID"
CC_PASSWORD="你的密码"
```

**详细教程：**[Cookie Cloud 配置指南](COOKIE_CLOUD_GUIDE.md)

---

### 7. Telegram 通知

**同步完成后自动推送详细报告到 Telegram**

每次同步结束后，Bot 会发送一条包含以下信息的报告：

- 同步状态（成功/警告/错误）和耗时
- 处理书籍数、新同步条数、累计同步条数
- AI 摘要和标签的生成统计
- 书籍详情（最多显示 5 本）
- 警告和错误信息（如有）

#### 配置

```yaml
# config.yaml
notification:
  telegram:
    enabled: true
```

```bash
# .env
TELEGRAM_BOT_TOKEN="你的Bot Token"
TELEGRAM_CHAT_ID="你的Chat ID"
# TELEGRAM_API_BASE="https://api.telegram.org"  # 可选，支持反代
```

#### 获取 Token 和 Chat ID

1. Telegram 搜索 [@BotFather](https://t.me/BotFather)，发送 `/newbot`，按提示创建 Bot，获取 `Bot Token`
2. 搜索 [@userinfobot](https://t.me/userinfobot)，发送任意消息获取你的 `Chat ID`
3. 向你创建的 Bot 发送一条消息（激活对话）
4. 将 Token 和 Chat ID 填入 `.env` 或 GitHub Secrets

> 通知功能为可选项，未配置时静默跳过，不影响同步流程。

---

### 8. 层级标签系统

**使用 Flomo 层级标签，更好地组织笔记**

#### 层级模式（推荐）

```
#微信读书/思考快与慢
#微信读书/番茄工作法图解
#微信读书/美丽新世界
```

**优势：**
- 更好的组织结构
- 在 Flomo 中自动分组
- 易于浏览和管理

#### 独立模式

```
#微信读书 #思考快与慢
#微信读书 #番茄工作法图解
#微信读书 #美丽新世界
```

#### 配置

```yaml
tags:
  use_hierarchical_tags: true  # 启用层级标签
  add_book_title: true  # 添加书名标签
  add_author: false  # 不添加作者标签
```

---

### 9. 时间筛选

**只同步指定时间范围内的划线**

#### 使用场景

- 初次使用，避免同步所有历史数据
- 定期同步，只关注最近阅读
- 控制同步量，避免超出 API 限制

#### 配置

```yaml
sync:
  days_limit: 100  # 只同步最近 100 天
```

或通过环境变量：

```bash
SYNC_DAYS_LIMIT=30  # 只同步最近 30 天
```

---

### 10. 增量同步

**智能去重，只同步新内容**

#### 工作原理

1. 记录已同步的划线 ID
2. 每次同步前检查记录
3. 跳过已同步的内容
4. 保存新同步的记录

#### 同步记录

```json
{
  "synced_ids": ["bookmark_id_1", "bookmark_id_2"],
  "last_sync": "2024-10-17T10:30:00",
  "total_synced": 150
}
```

#### 重新同步

如需重新同步所有内容：

```bash
rm synced_bookmarks.json
python sync.py
```

---

## 🎨 使用场景

### 场景 1：个人知识库

**目标：** 构建系统化的读书笔记库

**配置：**
- 使用**详细模板**
- 启用 **AI 摘要和标签**
- 开启**书籍分类**

```yaml
default_template: detailed
ai:
  enable_summary: true
tags:
  enable_ai_tags: true
  use_hierarchical_tags: true
```

### 场景 2：主题阅读

**目标：** 按主题整理阅读内容

**配置：**
- 使用**标准模板**
- 启用 **AI 标签**
- 自定义分类规则

```yaml
default_template: standard
tags:
  enable_ai_tags: true
book_categories:
  # 自定义分类...
```

### 场景 3：快速积累

**目标：** 快速记录，后续整理

**配置：**
- 使用**简洁模板**
- 禁用 AI 功能（降低成本）
- 最大化同步量

```yaml
default_template: simple
ai:
  provider: none
sync:
  max_highlights_per_sync: 100
```

### 场景 4：深度阅读

**目标：** 完整记录阅读过程

**配置：**
- 使用**详细模板**
- 同步笔记和划线
- 记录所有元数据

```yaml
default_template: detailed
sync:
  sync_reviews: true
  days_limit: 0  # 不限制时间
```

---

## 🔧 技术特性

### 高性能

- ✅ 智能缓存机制
- ✅ 批量处理优化
- ✅ 异步请求支持
- ✅ 增量同步减少数据传输

### 高可用

- ✅ 错误重试机制
- ✅ 优雅降级（AI 失败不影响同步）
- ✅ 详细日志记录
- ✅ 状态持久化

### 高扩展性

- ✅ 插件化架构
- ✅ 灵活的配置系统
- ✅ 模板自定义
- ✅ 易于添加新功能

### 安全性

- ✅ 本地数据处理
- ✅ 敏感信息加密
- ✅ 不上传第三方服务
- ✅ 支持私有化部署

---

## 📈 性能优化

### API 请求优化

```yaml
advanced:
  request_delay: 1.0  # 请求间隔（秒）
  max_retries: 3  # 重试次数
```

### 同步量控制

```yaml
sync:
  max_highlights_per_sync: 50  # 每次最多同步
  days_limit: 100  # 时间范围限制
```

### 日志级别

```yaml
advanced:
  log_level: "INFO"  # DEBUG/INFO/WARNING/ERROR
```

---

## 🔒 隐私保护

### 本地处理

所有数据在本地处理，不上传到第三方服务器。

### Cookie 安全

- Cookie Cloud 使用端对端加密
- 本地存储使用环境变量
- 不记录到代码仓库

### AI 隐私

- 支持使用私有 AI 服务
- 可以使用本地规则引擎（无需 API）
- AI 请求仅包含必要信息

---

## 🚀 未来规划

### 已完成 ✅

- [x] Telegram 同步报告通知
- [x] AI 智能摘要

### 短期（1-3个月）

- [ ] Web 管理界面
- [ ] 多账号支持
- [ ] 批量编辑和管理
- [ ] 更多模板预设

### 中期（3-6个月）

- [ ] 导出为 Markdown/PDF
- [ ] 支持 Notion
- [ ] 支持 Obsidian
- [ ] 移动端支持

### 长期（6-12个月）

- [ ] 知识图谱可视化
- [ ] 笔记关联和引用
- [ ] AI 对话式检索
- [ ] 社区模板市场

---

**更多功能持续开发中...** 🚀

