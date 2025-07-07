# 🚀 飞书文章自动发布到Twitter

一个基于飞书多维表格和Twitter API的自动发布工具，能够定时从飞书多维表格获取文章内容并自动发布到Twitter。

## ✨ 功能特性

- 📊 **飞书多维表格集成**：从飞书多维表格读取文章内容
- 🐦 **Twitter API集成**：使用官方API安全发布推文
- ⏰ **定时自动发布**：每天3次自动发布（8:00、14:00、20:00）
- 🔄 **智能内容管理**：自动标记已发布内容，避免重复
- 📝 **推文格式化**：自动格式化内容，确保符合Twitter字符限制
- 🤖 **GitHub Actions自动化**：无需服务器，完全基于GitHub Actions
- 📊 **日志记录**：完整的运行日志，便于调试和监控

## 🛠️ 技术栈

- **Python 3.11**
- **飞书开放平台API**
- **Twitter API v2**
- **GitHub Actions**
- **Tweepy**

## 📋 前置要求

### 1. 飞书配置
- 创建飞书应用获取 `App ID` 和 `App Secret`
- 创建多维表格并获取 `bitable_token` 和 `table_id`
- 确保应用有读写多维表格的权限

### 2. Twitter配置
- 申请Twitter开发者账户
- 创建应用获取API密钥和访问令牌
- 需要的密钥：`API Key`、`API Secret`、`Access Token`、`Access Token Secret`、`Bearer Token`

### 3. 飞书多维表格结构
确保您的飞书多维表格包含以下字段：
- `标题` (文本)
- `内容` (多行文本)
- `作者` (文本)
- `来源` (文本)
- `已发布` (复选框)

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/your-username/twitter_auto.git
cd twitter_auto
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置环境变量
复制 `config.env.example` 为 `.env` 并填入您的配置：
```bash
cp config.env.example .env
```

编辑 `.env` 文件：
```env
# Twitter API 配置
TWITTER_CONSUMER_KEY=your_twitter_consumer_key
TWITTER_CONSUMER_SECRET=your_twitter_consumer_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
TWITTER_BEARER_TOKEN=your_twitter_bearer_token

# 飞书API配置
FEISHU_APP_ID=your_feishu_app_id
FEISHU_APP_SECRET=your_feishu_app_secret
FEISHU_BITABLE_TOKEN=your_bitable_token
FEISHU_TABLE_ID=your_table_id

# 其他配置
TIMEZONE=Asia/Shanghai
DEBUG=False
```

### 4. 测试配置
```bash
python main.py test
```

### 5. 运行发布
```bash
python main.py run
```

## 📖 使用说明

### 命令行参数
- `test` - 测试模式，验证API连接和内容获取
- `status` - 查看系统状态
- `run` - 执行单次发布任务
- `schedule` - 定时任务模式（由GitHub Actions调用）

### 示例命令
```bash
# 测试API连接
python main.py test

# 查看系统状态
python main.py status

# 执行一次发布
python main.py run

# 定时任务（通常由GitHub Actions调用）
python main.py schedule
```

## ⚙️ GitHub Actions自动化

### 1. 设置GitHub Secrets
在您的GitHub仓库中，转到 `Settings` > `Secrets and variables` > `Actions`，添加以下secrets：

**Twitter API配置：**
- `TWITTER_CONSUMER_KEY`
- `TWITTER_CONSUMER_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_TOKEN_SECRET`
- `TWITTER_BEARER_TOKEN`

**飞书API配置：**
- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`
- `FEISHU_BITABLE_TOKEN`
- `FEISHU_TABLE_ID`

### 2. 启用GitHub Actions
- 项目会自动在每天的8:00、14:00、20:00（北京时间）执行发布任务
- 也可以手动触发工作流

### 3. 监控运行状态
- 在GitHub的Actions页面查看运行日志
- 失败时会自动上传日志文件

## 📊 推文格式

发布的推文将按以下格式排版：
```
📝 [文章标题]
[文章内容]
👤 [作者] | 📚 [来源]

#文章分享 #内容创作
```

## 🔧 自定义配置

### 修改发布频率
编辑 `.github/workflows/auto_publish.yml` 中的 `cron` 表达式：
```yaml
schedule:
  - cron: '0 0 * * *'  # 每天08:00
  - cron: '0 6 * * *'  # 每天14:00
  - cron: '0 12 * * *' # 每天20:00
```

### 修改推文格式
编辑 `connect_twitter.py` 中的 `format_tweet_content` 方法。

## 📝 日志管理

- 日志文件：`twitter_auto_bot.log`
- 日志级别：INFO
- 自动轮转：GitHub Actions会保留最近7天的日志

## 🚨 故障排查

### 常见问题

1. **API连接失败**
   - 检查API密钥是否正确
   - 确认网络连接正常
   - 验证权限配置

2. **找不到文章**
   - 检查飞书多维表格结构
   - 确认有未发布的内容
   - 验证字段名称匹配

3. **推文发布失败**
   - 检查推文内容是否符合Twitter规则
   - 确认API使用限制
   - 验证账户状态

### 调试模式
设置 `DEBUG=True` 启用调试模式，这样不会真正发布推文，只会显示格式化后的内容。

## 🔒 安全说明

- 所有敏感信息都存储在GitHub Secrets中
- 使用官方API，符合平台服务条款
- 代码开源，便于审计和改进

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 提交Pull Request

## 📄 许可证

MIT License

## 🙏 致谢

- 感谢飞书开放平台提供的API
- 感谢Twitter API的支持
- 参考了 [Chuchu_bot](https://github.com/EricLuceroGonzalez/Chuchu_bot) 项目的设计思路

---

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 提交Issue
- 发送邮件
- 微信群交流

**享受自动化发布的便利！** 🎉 