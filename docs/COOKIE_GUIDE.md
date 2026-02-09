# 手动获取微信读书 Cookie

> 推荐使用 [Cookie Cloud](COOKIE_CLOUD_GUIDE.md) 自动同步 Cookie，免去手动操作。以下为手动获取方式。

---

## 获取步骤

### 方法 1：从 Application 标签获取（推荐）

1. 打开 [微信读书网页版](https://weread.qq.com/)，微信扫码登录
2. 按 **F12** 打开开发者工具
3. 切换到 **Application** 标签（Chrome）或 **存储** 标签（Firefox）
4. 展开左侧 `Cookies` → 点击 `https://weread.qq.com`
5. 确认以下关键字段存在且非空：

| Cookie 字段 | 说明 |
|-------------|------|
| `wr_skey` | 认证密钥（最重要） |
| `wr_vid` | 用户 ID |
| `RK` | 认证令牌 |

6. 复制所有 Cookie 值，填入 `.env` 的 `WEREAD_COOKIE`

### 方法 2：从 Network 标签获取

1. 登录微信读书网页版
2. 按 **F12** → 切换到 **Network** 标签
3. 刷新页面
4. 点击任意请求 → **Headers** → 找到 `Cookie` 字段
5. 复制完整的 Cookie 值

### 方法 3：控制台脚本获取

在浏览器控制台（Console 标签）运行：

```javascript
// 检查关键 Cookie 并复制
const cookies = document.cookie.split('; ').map(c => {
  const [key, value] = c.split('=');
  return { key, value };
});

console.log('🔑 关键 Cookie 检查:');
['wr_skey', 'wr_vid', 'RK'].forEach(field => {
  const cookie = cookies.find(c => c.key === field);
  console.log(cookie ? `✓ ${field}: ${cookie.value}` : `✗ ${field}: 缺失`);
});

copy(document.cookie);
console.log('✅ Cookie 已复制到剪贴板！');
```

---

## 验证 Cookie 是否有效

获取 Cookie 后，运行验证脚本：

```bash
python tests/verify_cookie.py
```

或在浏览器控制台测试：

```javascript
fetch('https://i.weread.qq.com/user/notebooks', {
  credentials: 'include',
  headers: { 'Accept': 'application/json' }
})
.then(r => r.json())
.then(data => {
  if (data.books) {
    console.log('✅ Cookie 有效！找到', data.books.length, '本书');
  } else {
    console.log('❌ Cookie 无效:', data);
  }
});
```

---

## 常见问题

**Q: Cookie 多久会过期？**

微信读书 Cookie 有效期较短（通常数小时到数天），且在其他设备登录时可能失效。推荐使用 [Cookie Cloud](COOKIE_CLOUD_GUIDE.md) 自动同步。

**Q: 浏览器显示已登录，但 Cookie 验证失败？**

浏览器可能使用了本地缓存。尝试：
1. 硬刷新页面（Ctrl+Shift+R）
2. 如果仍无效，退出登录后重新扫码登录
3. 登录后立即获取 Cookie

**Q: 能自动更新 Cookie 吗？**

可以，使用 [Cookie Cloud](COOKIE_CLOUD_GUIDE.md) 配合浏览器插件即可自动同步，无需手动操作。
