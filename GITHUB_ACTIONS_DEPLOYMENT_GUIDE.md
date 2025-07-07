# GitHub Actions 部署指南

本指南将帮助您将Twitter自动发布机器人部署到GitHub Actions，实现自动化运行。

## 🚀 部署步骤

### 1. 准备GitHub仓库

1. 将项目代码推送到GitHub仓库
2. 确保包含以下必要文件：
   - `main.py` - 主程序
   - `requirements.txt` - 依赖包列表
   - `.github/workflows/` - GitHub Actions工作流文件

### 2. 配置GitHub Secrets

在GitHub仓库中配置以下机密信息：

#### 2.1 进入仓库设置
1. 打开GitHub仓库页面
2. 点击 `Settings` 标签
3. 在左侧菜单中选择 `Secrets and variables` > `Actions`
4. 点击 `New repository secret`

#### 2.2 需要配置的Secrets

**Twitter API 配置：**
- `TWITTER_CONSUMER_KEY` - Twitter API消费者密钥
- `TWITTER_CONSUMER_SECRET` - Twitter API消费者密钥密码
- `TWITTER_ACCESS_TOKEN` - Twitter访问令牌
- `TWITTER_ACCESS_TOKEN_SECRET` - Twitter访问令牌密码
- `TWITTER_BEARER_TOKEN` - Twitter Bearer令牌

**飞书API配置：**
- `FEISHU_APP_ID` - 飞书应用ID
- `FEISHU_APP_SECRET` - 飞书应用密钥
- `FEISHU_BITABLE_TOKEN` - 飞书多维表格令牌
- `FEISHU_TABLE_ID` - 飞书表格ID

#### 2.3 获取API密钥步骤

**Twitter API：**
1. 访问 [Twitter Developer Portal](https://developer.twitter.com/)
2. 创建新的应用程序
3. 生成API密钥和访问令牌
4. 复制所有必需的密钥

**飞书API：**
1. 访问 [飞书开发者平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 获取App ID和App Secret
4. 创建多维表格并获取Token和Table ID

### 3. 工作流说明

#### 3.1 定时发布工作流 (`schedule_publish.yml`)

**功能：**
- 自动定时发布Twitter内容
- 每天北京时间 6:00, 12:00, 18:00, 24:00 执行
- 支持手动触发

**时间设置：**
```yaml
schedule:
  # 每天北京时间 6:00, 12:00, 18:00, 24:00 执行 (UTC时间 22:00, 4:00, 10:00, 16:00)
  - cron: '0 22,4,10,16 * * *'
```

**手动触发：**
1. 进入仓库的 `Actions` 页面
2. 选择 `定时发布Twitter内容` 工作流
3. 点击 `Run workflow` 按钮
4. 选择是否开启调试模式
5. 点击 `Run workflow` 执行

#### 3.2 手动发布工作流 (`manual_publish.yml`)

**功能：**
- 手动触发发布任务
- 支持测试、发布、状态检查等操作
- 支持调试模式

**使用方法：**
1. 进入仓库的 `Actions` 页面
2. 选择 `手动发布Twitter内容` 工作流
3. 点击 `Run workflow` 按钮
4. 选择执行的操作：
   - `test` - 测试API连接
   - `run` - 执行单次发布
   - `status` - 检查机器人状态
5. 选择是否开启调试模式
6. 点击 `Run workflow` 执行

### 4. 监控和日志

#### 4.1 查看执行日志

1. 进入仓库的 `Actions` 页面
2. 点击具体的工作流运行记录
3. 查看详细的执行日志

#### 4.2 下载日志文件

1. 在工作流运行完成后，会自动生成日志文件
2. 在工作流运行页面的 `Artifacts` 部分可以下载日志文件
3. 日志文件保留7天

### 5. 故障排除

#### 5.1 常见问题

**API连接失败：**
- 检查GitHub Secrets是否正确配置
- 验证API密钥是否有效
- 确认网络连接正常

**发布失败：**
- 检查飞书表格中是否有待发布的内容
- 验证Twitter API配额是否充足
- 查看详细日志了解具体错误

**权限问题：**
- 确保Twitter API有发布权限
- 检查飞书应用是否有访问表格的权限

#### 5.2 调试技巧

1. 使用调试模式运行工作流
2. 查看详细的日志输出
3. 下载日志文件进行离线分析
4. 使用测试模式验证API连接

### 6. 自定义设置

#### 6.1 修改发布时间

编辑 `.github/workflows/schedule_publish.yml` 文件中的 cron 表达式：

```yaml
schedule:
  # 自定义时间，例如每4小时执行一次
  - cron: '0 */4 * * *'
  # 或者每天特定时间，例如早上8点和晚上8点（UTC时间0点和12点）
  - cron: '0 0,12 * * *'
```

#### 6.2 添加通知

可以在工作流中添加通知步骤，例如发送邮件或Slack消息：

```yaml
- name: 发送通知
  if: failure()
  run: |
    # 在这里添加通知逻辑
    echo "发布失败，请检查日志"
```

### 7. 安全建议

1. **定期更新密钥：** 定期更新Twitter和飞书API密钥
2. **最小权限原则：** 仅赋予必要的API权限
3. **监控使用：** 定期检查API使用情况
4. **备份配置：** 保留配置文件的备份

## 🎯 快速启动清单

- [ ] 创建GitHub仓库并推送代码
- [ ] 配置所有必需的GitHub Secrets
- [ ] 测试API连接（运行手动工作流的test模式）
- [ ] 验证定时任务正常工作
- [ ] 设置监控和告警

## 📞 获取帮助

如果遇到问题，请：
1. 检查GitHub Actions的执行日志
2. 查看项目README文件
3. 验证API密钥配置是否正确
4. 确保飞书表格中有待发布的内容

---

**注意：** 请确保遵守Twitter和飞书的使用条款，合理使用API配额。 