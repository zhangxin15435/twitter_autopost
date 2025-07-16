# 🛠️ 手动发布故障排除指南

## 📋 常见问题和解决方案

### 🔍 问题1：依赖包缺失错误

**错误信息：**
```
ModuleNotFoundError: No module named 'tweepy'
ModuleNotFoundError: No module named 'dotenv'
```

**解决方案：**
✅ **已修复** - 我们已经更新了GitHub Actions工作流，现在总是安装依赖包。

---

### 🔍 问题2：账号禁用导致发布失败

**错误信息：**
```
账号 'ContextSpace' 配置未找到或所有相关账号已禁用
```

**解决方案：**
```bash
# 方案A：临时启用ContextSpace账号测试
python manage_accounts.py --enable contextspace

# 方案B：使用其他启用的账号
# 选择 'Ai flow watch' 或 'OSS Discoveries'
```

**当前状态：** ✅ ContextSpace已临时启用供测试

---

### 🔍 问题3：GitHub Actions YAML格式错误

**错误信息：**
```
Workflow syntax error
Invalid step definition
```

**解决方案：**
✅ **已修复** - 已重写 `manual_publish.yml` 文件，修复所有格式问题。

---

### 🔍 问题4：API密钥配置问题

**错误信息：**
```
401 Unauthorized
403 Forbidden
```

**解决方案：**
1. 检查GitHub Secrets中的API密钥是否正确
2. 确认Twitter账号的API权限
3. 验证Bearer Token是否有效

---

## 🚀 测试步骤

### 1. 测试依赖验证
在GitHub Actions中应该看到：
```
🧪 验证关键依赖包...
✅ tweepy - Twitter API库
✅ python-dotenv - 环境变量加载库
✅ requests - HTTP请求库
✅ pandas - 数据处理库
✅ pytz - 时区处理库
🎉 所有关键依赖验证通过！
```

### 2. 测试账号连接
应该看到：
```
📋 账号连接状态:
   ✅ contextspace (@username)
   ✅ aiflowwatch (@username)
   ✅ ossdiscoveries (@username)
```

### 3. 测试手动发布
**调试模式测试：**
- 推文内容：`测试推文 #test`
- 目标账号：`ContextSpace`
- 调试模式：`true`

**正式发布测试：**
- 推文内容：`Hello from automated system! 🤖`
- 目标账号：`ContextSpace`
- 调试模式：`false`

---

## 🔧 快速修复命令

### 重新启用ContextSpace账号
```bash
cd twitter_autopost
python -c "
import json
status = {'contextspace': True, 'ossdiscoveries': True, 'aiflowwatch': True, 'opensourcereader': True, 'default': True}
with open('twitter_accounts_status.json', 'w') as f:
    json.dump(status, f, indent=2)
print('✅ ContextSpace账号已启用')
"
```

### 验证账号状态
```bash
python manage_accounts.py --status
```

### 测试本地手动发布（调试模式）
```bash
python manual_publish.py --content "测试推文" --account "ContextSpace" --debug
```

---

## 📊 预期的成功输出

### GitHub Actions成功运行应显示：

```
📥 检出代码 ✅
🐍 设置Python环境 ✅  
📦 安装依赖 ✅
🔍 验证关键依赖 ✅
📝 显示发布信息 ✅
🔍 调试账号配置 ✅
🚀 执行手动推文发布 ✅
📊 上传执行日志 ✅
📋 发布结果总结 ✅
```

### 成功发布的日志：
```
🎉 推文发布成功！
   账号: @username
   推文ID: 1234567890
   链接: https://twitter.com/username/status/1234567890
```

---

## 🆘 如果仍然失败

### 1. 检查GitHub Actions日志
- 进入Actions页面
- 查看失败的step
- 复制完整错误信息

### 2. 检查API密钥
确保以下Secrets正确配置：
```
TWITTER_CONTEXTSPACE_CONSUMER_KEY
TWITTER_CONTEXTSPACE_CONSUMER_SECRET  
TWITTER_CONTEXTSPACE_ACCESS_TOKEN
TWITTER_CONTEXTSPACE_ACCESS_TOKEN_SECRET
TWITTER_CONTEXTSPACE_BEARER_TOKEN
```

### 3. 联系支持
提供以下信息：
- GitHub Actions运行ID
- 完整错误日志
- 使用的推文内容和目标账号

---

## 💡 提示

1. **优先使用调试模式测试** - 不会实际发布，安全验证流程
2. **一次只测试一个账号** - 便于排查问题
3. **注意字符限制** - 推文内容不超过280字符
4. **检查网络连接** - GitHub Actions需要访问Twitter API

---

## ✅ 当前修复状态

- ✅ 依赖包安装问题已修复
- ✅ YAML格式错误已修复  
- ✅ ContextSpace账号已临时启用
- ✅ 增加了详细的错误日志
- ✅ 添加了依赖验证步骤

**现在可以重新测试手动发布功能！** 🚀 