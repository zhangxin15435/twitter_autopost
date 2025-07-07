# 📋 详细配置指南

本指南将帮助您完成飞书和Twitter API的配置，实现自动发布功能。

## 🔧 飞书配置

### 1. 创建飞书应用

1. 访问[飞书开放平台](https://open.feishu.cn/)
2. 登录您的飞书账户
3. 点击"创建应用"
4. 选择"企业自建应用"
5. 填写应用信息：
   - 应用名称：例如"Twitter自动发布"
   - 应用描述：文章自动发布工具
   - 应用图标：选择合适的图标

### 2. 获取应用凭证

1. 在应用详情页面，找到"凭证与基础信息"
2. 记录以下信息：
   - `App ID`：应用ID
   - `App Secret`：应用密钥

### 3. 配置应用权限

1. 在应用管理页面，点击"权限管理"
2. 添加以下权限：
   - `bitable:app`：多维表格应用权限
   - `bitable:app:readonly`：多维表格只读权限
   - `bitable:app:write`：多维表格写入权限

### 4. 创建多维表格

1. 在飞书中创建一个新的多维表格
2. 设置表格结构，包含以下字段：

| 字段名 | 类型 | 说明 | 必填 |
|--------|------|------|------|
| 标题 | 文本 | 文章标题 | ✅ |
| 内容 | 多行文本 | 文章内容 | ✅ |
| 作者 | 文本 | 文章作者 | ❌ |
| 来源 | 文本 | 文章来源 | ❌ |
| 已发布 | 复选框 | 是否已发布 | ✅ |

### 5. 获取多维表格信息

1. 打开创建的多维表格
2. 从浏览器地址栏获取以下信息：
   - URL格式：`https://your-domain.feishu.cn/base/bitable_token?table=table_id`
   - `bitable_token`：多维表格令牌（base/后面的部分）
   - `table_id`：表格ID（table=后面的部分）

### 6. 发布应用

1. 回到应用管理页面
2. 点击"版本管理与发布"
3. 创建版本并发布
4. 在"可用性状态"中启用应用

## 🐦 Twitter API配置

### 1. 申请Twitter开发者账户

1. 访问[Twitter Developer Portal](https://developer.twitter.com/)
2. 使用您的Twitter账户登录
3. 点击"Apply for a developer account"
4. 填写申请表单：
   - 选择用途：例如"Building tools for Twitter"
   - 描述用途：自动化内容发布工具
   - 不会分析Twitter数据
   - 不会显示推文内容给其他用户

### 2. 等待审核

- 通常需要1-7天审核时间
- 可能需要回答补充问题
- 审核通过后会收到邮件通知

### 3. 创建应用

1. 登录Twitter Developer Portal
2. 点击"Create an App"
3. 填写应用信息：
   - App name：例如"Auto Publisher"
   - App description：自动发布工具
   - Website URL：您的GitHub仓库地址
   - App usage：描述应用用途

### 4. 获取API密钥

1. 在应用详情页面，找到"Keys and tokens"
2. 记录以下信息：
   - `API Key`：消费者密钥（Consumer Key）
   - `API Secret Key`：消费者密钥密码（Consumer Secret）
   - `Bearer Token`：承载令牌

### 5. 生成访问令牌

1. 在"Keys and tokens"页面
2. 点击"Generate Access Token and Secret"
3. 记录以下信息：
   - `Access Token`：访问令牌
   - `Access Token Secret`：访问令牌密码

### 6. 配置应用权限

1. 在应用设置中，确保权限设置为：
   - `Read and Write`：读写权限
   - 如果需要发布媒体，还需要`Read, Write, and Direct Messages`

## 🔐 GitHub Secrets配置

### 1. 进入仓库设置

1. 在GitHub仓库页面，点击"Settings"
2. 在左侧菜单中选择"Secrets and variables"
3. 点击"Actions"

### 2. 添加Secrets

点击"New repository secret"，逐一添加以下secrets：

#### Twitter API配置
- **Name**: `TWITTER_CONSUMER_KEY`
  - **Value**: 您的Twitter Consumer Key
- **Name**: `TWITTER_CONSUMER_SECRET`
  - **Value**: 您的Twitter Consumer Secret
- **Name**: `TWITTER_ACCESS_TOKEN`
  - **Value**: 您的Twitter Access Token
- **Name**: `TWITTER_ACCESS_TOKEN_SECRET`
  - **Value**: 您的Twitter Access Token Secret
- **Name**: `TWITTER_BEARER_TOKEN`
  - **Value**: 您的Twitter Bearer Token

#### 飞书API配置
- **Name**: `FEISHU_APP_ID`
  - **Value**: 您的飞书App ID
- **Name**: `FEISHU_APP_SECRET`
  - **Value**: 您的飞书App Secret
- **Name**: `FEISHU_BITABLE_TOKEN`
  - **Value**: 您的多维表格Token
- **Name**: `FEISHU_TABLE_ID`
  - **Value**: 您的表格ID

## 🧪 测试配置

### 1. 本地测试

1. 创建`.env`文件（参考`config.env.example`）
2. 填入您的配置信息
3. 运行测试命令：
   ```bash
   python main.py test
   ```

### 2. 测试输出示例

成功的测试输出应该如下：
```
✅ API连接测试通过
✅ 成功获取文章: 示例文章标题
✅ 推文内容预览:
📝 示例文章标题
这是一篇示例文章的内容...
👤 作者名称 | 📚 来源名称

#文章分享 #内容创作
✅ 推文长度: 120 字符
```

### 3. GitHub Actions测试

1. 在GitHub仓库中，转到"Actions"页面
2. 点击"自动发布文章到Twitter"工作流
3. 点击"Run workflow"
4. 选择"test"模式
5. 点击"Run workflow"

## 🚨 常见问题

### 飞书相关问题

**Q: 无法获取访问令牌**
- A: 检查App ID和App Secret是否正确
- A: 确认应用已发布并启用

**Q: 无法读取多维表格**
- A: 检查bitable_token和table_id是否正确
- A: 确认应用有多维表格权限

**Q: 找不到未发布的文章**
- A: 检查表格中是否有"已发布"字段为False的记录
- A: 确认字段名称与代码中一致

### Twitter相关问题

**Q: API连接失败**
- A: 检查所有API密钥是否正确填写
- A: 确认Twitter开发者账户状态正常

**Q: 推文发布失败**
- A: 检查推文内容是否符合Twitter规则
- A: 确认账户没有被限制
- A: 检查API使用限制

**Q: 403 Forbidden错误**
- A: 确认应用权限设置为Read and Write
- A: 检查Access Token是否有效

## 📞 获取帮助

如果您在配置过程中遇到问题：

1. 查看项目的Issues页面
2. 提交新的Issue，详细描述问题
3. 在Issue中包含相关的日志信息（请勿包含敏感信息）

## 🎯 下一步

配置完成后，您可以：

1. 在飞书多维表格中添加文章内容
2. 运行本地测试确认功能正常
3. 等待GitHub Actions自动执行
4. 监控发布状态和日志

---

**祝您配置顺利！** 🎉 