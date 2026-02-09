# GitHub Secrets 配置指南

GitHub Actions 中有两种配置 secrets 的方式，很多人容易混淆。本文档帮你理解区别并选择合适的方式。

---

## 📊 两种 Secrets 对比

| 特性 | Repository Secrets | Environment Secrets |
|------|-------------------|---------------------|
| **配置路径** | Settings → Secrets and variables → Actions | Settings → Environments → 环境名 → Secrets |
| **使用方式** | 直接在 workflow 中使用 | 需要在 job 中指定 environment |
| **适用场景** | 简单项目，单一环境 | 多环境（开发/测试/生产） |
| **访问控制** | 所有 workflow 都能访问 | 只有指定 environment 的 job 能访问 |
| **推荐度** | ⭐⭐⭐⭐⭐ 推荐（简单） | ⭐⭐⭐ 复杂项目使用 |

---

## 🎯 方案选择

### 方案 A：使用 Repository Secrets（推荐）

**适合：** 大多数用户，简单直接

**配置步骤：**

1. 进入仓库 `Settings` 标签
2. 左侧菜单选择 `Secrets and variables` → `Actions`
3. 点击 `New repository secret`
4. 逐个添加以下 secrets：

| Name | Value |
|------|-------|
| `CC_URL` | `https://cc.chenge.ink` |
| `CC_ID` | 你的 Cookie Cloud UUID |
| `CC_PASSWORD` | 你的 Cookie Cloud 密码 |
| `WEREAD_COOKIE` | 你的微信读书 Cookie（备用） |
| `FLOMO_API` | 你的 Flomo API 地址 |
| `AI_API_KEY` | 你的 AI API Key（可选） |
| `TELEGRAM_BOT_TOKEN` | 你的 Telegram Bot Token（可选） |
| `TELEGRAM_CHAT_ID` | 你的 Telegram Chat ID（可选） |

**Workflow 配置：**

```yaml
jobs:
  sync:
    runs-on: ubuntu-latest
    # 不需要指定 environment
    
    steps:
    - name: 运行同步
      env:
        CC_URL: ${{ secrets.CC_URL }}
        CC_ID: ${{ secrets.CC_ID }}
        # ... 其他 secrets
```

---

### 方案 B：使用 Environment Secrets

**适合：** 需要多环境管理的复杂项目

**配置步骤：**

1. 进入仓库 `Settings` 标签
2. 左侧菜单选择 `Environments`
3. 点击 `New environment`，创建环境（如 `production`）
4. 进入环境，点击 `Add secret`
5. 添加所有需要的 secrets

**Workflow 配置（重要！）：**

```yaml
jobs:
  sync:
    runs-on: ubuntu-latest
    environment: production  # ⭐ 必须指定 environment
    
    steps:
    - name: 运行同步
      env:
        CC_URL: ${{ secrets.CC_URL }}
        CC_ID: ${{ secrets.CC_ID }}
        # ... 其他 secrets
```

**关键点**：
- ⚠️ **必须添加 `environment: 环境名`**
- ⚠️ 环境名要和你创建的环境名称一致
- ⚠️ 如果不指定 environment，secrets 将读取不到（都是空值）

---

## 🐛 常见问题

### Q1: 我的 secrets 都是空的！

**症状：**
```bash
CC_URL=""
CC_ID=""
FLOMO_API=""
# 所有值都是空的
```

**可能原因：**

1. **使用了 Environment Secrets 但没有指定 environment**
   ```yaml
   # ❌ 错误
   jobs:
     sync:
       runs-on: ubuntu-latest
       # 缺少 environment 配置！
   
   # ✅ 正确
   jobs:
     sync:
       runs-on: ubuntu-latest
       environment: env  # 添加这一行
   ```

2. **Secrets 名称拼写错误**
   ```yaml
   # Secret 名称是 CC_URL，但写成了 CC_url
   CC_URL: ${{ secrets.CC_url }}  # ❌ 错误（大小写不对）
   CC_URL: ${{ secrets.CC_URL }}  # ✅ 正确
   ```

3. **Secrets 没有保存**
   - 确认在 Settings 中能看到已添加的 secrets
   - Secrets 添加后名称会显示，但值是隐藏的

### Q2: 如何验证 secrets 是否正确？

**方法 1：查看 Actions 日志**

正确配置后，日志中 secrets 的值会被隐藏为 `***`：

```bash
# ✅ 正确（值被隐藏）
CC_URL="***"
CC_ID="***"
FLOMO_API="***"

# ❌ 错误（值是空的）
CC_URL=""
CC_ID=""
FLOMO_API=""
```

**方法 2：添加调试步骤**

在 workflow 中添加：

```yaml
- name: 🔍 验证环境变量（调试）
  run: |
    echo "CC_URL is set: ${{ secrets.CC_URL != '' }}"
    echo "FLOMO_API is set: ${{ secrets.FLOMO_API != '' }}"
    # 注意：不要直接 echo secrets 的值！会泄露！
```

### Q3: Repository Secrets 和 Environment Secrets 可以混用吗？

可以，但不推荐！容易混淆。

**优先级：**
```
Environment Secrets > Repository Secrets
```

如果同名，Environment Secrets 会覆盖 Repository Secrets。

### Q4: 我已经配置了 Environment，为什么还是读不到？

检查清单：

1. ✅ Environment 名称拼写正确（区分大小写）
2. ✅ Workflow 中添加了 `environment: 环境名`
3. ✅ Secrets 名称和 workflow 中引用的名称一致
4. ✅ 重新运行 workflow（不是重新运行旧的记录）

---

## 🎯 推荐配置（本项目）

### 如果你是新用户（推荐）

**使用 Repository Secrets：**

1. 删除 Environments 中的配置（如果有）
2. 在 Repository Secrets 中添加所有 secrets
3. Workflow 文件保持当前配置（已包含 `environment: env`，需要删除）

**修改 workflow：**

```yaml
jobs:
  sync:
    runs-on: ubuntu-latest
    # environment: env  # 删除或注释这一行
```

### 如果你已经配置了 Environment Secrets

**保持当前配置：**

1. Environment 名称：`env`
2. Workflow 已添加：`environment: env` ✅
3. 在 Environment 中确保所有 secrets 都已添加
4. 重新运行 workflow

---

## 📝 完整示例

### 示例 1：使用 Repository Secrets

**Settings 配置：**
```
Settings → Secrets and variables → Actions
├── CC_URL = "https://cc.chenge.ink"
├── CC_ID = "your-uuid"
├── CC_PASSWORD = "your-password"
├── FLOMO_API = "https://flomoapp.com/iwh/..."
├── AI_API_KEY = "sk-..."
├── TELEGRAM_BOT_TOKEN = "123456:ABC..."
└── TELEGRAM_CHAT_ID = "123456789"
```

**Workflow 配置：**
```yaml
jobs:
  sync:
    runs-on: ubuntu-latest
    # 不需要 environment
    
    steps:
    - name: 运行同步
      env:
        CC_URL: ${{ secrets.CC_URL }}
        CC_ID: ${{ secrets.CC_ID }}
        CC_PASSWORD: ${{ secrets.CC_PASSWORD }}
        FLOMO_API: ${{ secrets.FLOMO_API }}
        AI_API_KEY: ${{ secrets.AI_API_KEY }}
        TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
        TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
      run: python sync.py
```

### 示例 2：使用 Environment Secrets

**Settings 配置：**
```
Settings → Environments → env → Secrets
├── CC_URL = "https://cc.chenge.ink"
├── CC_ID = "your-uuid"
├── CC_PASSWORD = "your-password"
├── FLOMO_API = "https://flomoapp.com/iwh/..."
├── AI_API_KEY = "sk-..."
├── TELEGRAM_BOT_TOKEN = "123456:ABC..."
└── TELEGRAM_CHAT_ID = "123456789"
```

**Workflow 配置：**
```yaml
jobs:
  sync:
    runs-on: ubuntu-latest
    environment: env  # ⭐ 必须指定
    
    steps:
    - name: 运行同步
      env:
        CC_URL: ${{ secrets.CC_URL }}
        CC_ID: ${{ secrets.CC_ID }}
        CC_PASSWORD: ${{ secrets.CC_PASSWORD }}
        FLOMO_API: ${{ secrets.FLOMO_API }}
        AI_API_KEY: ${{ secrets.AI_API_KEY }}
        TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
        TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
      run: python sync.py
```

---

## 🔒 安全建议

1. ✅ **永远不要在日志中打印 secrets**
   ```yaml
   # ❌ 危险！
   - run: echo "My secret is ${{ secrets.MY_SECRET }}"
   
   # ✅ 安全
   - run: echo "Secret is configured"
   ```

2. ✅ **定期更换敏感信息**
   - Cookie 定期失效，需要更新
   - API Key 建议定期更换
   - 密码建议使用强密码

3. ✅ **使用 Environment 保护规则**
   - 设置审批流程（可选）
   - 限制分支访问
   - 添加等待时间

4. ✅ **最小权限原则**
   - 只添加必需的 secrets
   - 不要共享 secrets
   - 使用只读 token（如果可能）

---

## 📚 相关文档

- [GitHub Actions - Using secrets](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions)
- [GitHub Actions - Using environments](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)
- [Cookie Cloud 配置指南](COOKIE_CLOUD_GUIDE.md)

---

## 🎉 总结

配置完成后，重新运行 workflow，secrets 值在日志中应显示为 `***`（而非空值），同步即可正常工作。

---