# GitHub Actions 四账号自动发布配置指南

## 🚀 快速开始

您的项目已完全支持四账号自动发布！按以下步骤配置即可启用：

### 📋 第一步：配置 GitHub Secrets

在 GitHub 仓库的 **Settings > Secrets and variables > Actions** 中添加：

#### 必需配置（四个Twitter账号）：

**1. ContextSpace主账号：**
```
TWITTER_CONTEXTSPACE_CONSUMER_KEY = ContextSpace的API密钥
TWITTER_CONTEXTSPACE_CONSUMER_SECRET = ContextSpace的API密钥密码
TWITTER_CONTEXTSPACE_ACCESS_TOKEN = ContextSpace的访问令牌
TWITTER_CONTEXTSPACE_ACCESS_TOKEN_SECRET = ContextSpace的访问令牌密码
TWITTER_CONTEXTSPACE_BEARER_TOKEN = ContextSpace的Bearer令牌
```

**2. OSS Discoveries账号：**
```
TWITTER_OSSDISCOVERIES_CONSUMER_KEY = OSS Discoveries的API密钥
TWITTER_OSSDISCOVERIES_CONSUMER_SECRET = OSS Discoveries的API密钥密码
TWITTER_OSSDISCOVERIES_ACCESS_TOKEN = OSS Discoveries的访问令牌
TWITTER_OSSDISCOVERIES_ACCESS_TOKEN_SECRET = OSS Discoveries的访问令牌密码
TWITTER_OSSDISCOVERIES_BEARER_TOKEN = OSS Discoveries的Bearer令牌
```

**3. AI Flow Watch账号：**
```
TWITTER_AIFLOWWATCH_CONSUMER_KEY = AI Flow Watch的API密钥
TWITTER_AIFLOWWATCH_CONSUMER_SECRET = AI Flow Watch的API密钥密码
TWITTER_AIFLOWWATCH_ACCESS_TOKEN = AI Flow Watch的访问令牌
TWITTER_AIFLOWWATCH_ACCESS_TOKEN_SECRET = AI Flow Watch的访问令牌密码
TWITTER_AIFLOWWATCH_BEARER_TOKEN = AI Flow Watch的Bearer令牌
```

**4. Open Source Reader账号：**
```
TWITTER_OPENSOURCEREADER_CONSUMER_KEY = Open Source Reader的API密钥
TWITTER_OPENSOURCEREADER_CONSUMER_SECRET = Open Source Reader的API密钥密码
TWITTER_OPENSOURCEREADER_ACCESS_TOKEN = Open Source Reader的访问令牌
TWITTER_OPENSOURCEREADER_ACCESS_TOKEN_SECRET = Open Source Reader的访问令牌密码
TWITTER_OPENSOURCEREADER_BEARER_TOKEN = Open Source Reader的Bearer令牌
```

### 🎯 第二步：内容账号映射

系统会自动根据CSV表格中的"发布账号"字段选择Twitter账号：

| CSV中的发布账号 | 目标Twitter账号 | 内容类型 |
|---|---|---|
| `ContextSpace` 或 `twitter` | @ContextSpace | 综合内容、主要发布 |
| `OSS Discoveries` | @OSSDiscoveries | 开源工具发现 |
| `Ai flow watch` | @AIFlowWatch | AI技术、机器学习 |
| `Open source reader` | @OpenSourceReader | 开源项目解读 |

### ⚙️ 第三步：工作流配置

#### 当前可用的 GitHub Actions：

1. **`auto_publish_multi_account.yml`** - 四账号自动发布
   - 每天北京时间20:00自动执行
   - 支持手动触发
   - 自动选择对应账号发布

2. **`schedule_publish.yml`** - 定时批量发布
   - 每天4次定时发布
   - 时间: 6:00, 12:00, 18:00, 24:00

#### 自定义发布时间：

修改 `.github/workflows/auto_publish_multi_account.yml` 文件中的 `cron` 表达式：

```yaml
on:
  schedule:
    # ContextSpace主账号: 每天晚上9点
    - cron: '0 13 * * *'   # UTC 13:00 = 北京时间 21:00
    
    # OSS Discoveries: 周末上午11点
    - cron: '0 3 * * 6'    # UTC 03:00 = 北京时间 11:00
    
    # AI Flow Watch: 工作日上午10点
    - cron: '0 2 * * 1-5'  # UTC 02:00 = 北京时间 10:00
    
    # Open Source Reader: 工作日下午3点
    - cron: '0 7 * * 1-5'  # UTC 07:00 = 北京时间 15:00
```

### 📊 第四步：当前内容状态

根据分析，您的内容分布：

- **总内容**: 11条
- **已发布**: 2条
- **待发布**: 9条

按账号分布：
- **ContextSpace**: 综合内容
- **OSS Discoveries**: 开源工具发现
- **AI Flow Watch**: AI技术内容
- **Open Source Reader**: 开源项目解读

### 🚀 第五步：运行和测试

#### 手动触发测试：
1. 进入 GitHub 仓库的 `Actions` 页面
2. 选择 `Twitter多账号自动发布` 工作流
3. 点击 `Run workflow` 按钮
4. 点击 `Run workflow` 执行

#### 本地测试：
```bash
# 测试四账号配置
python connect_twitter_multi.py

# 运行设置向导
python setup_multi_account_matrix.py

# 单次发布测试
python main_multi_account.py
```

### 📈 第六步：账号发布策略

#### 🏆 推荐四账号策略
适合：内容量大、有明确受众分类

1. **@ContextSpace** - 主账号
   - 综合内容发布
   - 每日2-3条
   - 晚上20:00-22:00发布

2. **@OSSDiscoveries** - 工具发现
   - 开源工具推荐
   - 每日1条
   - 周末10:00-12:00发布

3. **@AIFlowWatch** - AI技术
   - AI、机器学习内容
   - 每日1-2条
   - 工作日09:00-11:00发布

4. **@OpenSourceReader** - 项目解读
   - 开源项目深度分析
   - 每日1条
   - 工作日14:00-16:00发布

### 🔧 第七步：高级配置

#### 批量发布模式：

修改工作流以支持批量发布：

```yaml
- name: 批量发布四账号内容
  run: |
    python -c "
    from main_multi_account import MultiAccountTwitterPublisher
    publisher = MultiAccountTwitterPublisher()
    results = publisher.run_batch(max_posts=4)  # 每次最多发布4条
    print(f'发布结果: {results}')
    "
```

#### 账号轮询发布：

确保每个账号都有内容发布：

```yaml
- name: 四账号轮询发布
  run: |
    python -c "
    from main_multi_account import MultiAccountTwitterPublisher
    publisher = MultiAccountTwitterPublisher()
    accounts = ['ContextSpace', 'OSS Discoveries', 'Ai flow watch', 'Open source reader']
    for account in accounts:
        articles = publisher.get_next_articles_by_account()
        if account.lower() in [k.lower() for k in articles.keys()]:
            article = next(iter(articles[account]))
            publisher.publish_article(article)
            print(f'为账号 {account} 发布内容')
    "
```

### 📊 第八步：监控和优化

#### 查看发布状态：
```bash
# 查看详细统计
python -c "
from main_multi_account import MultiAccountTwitterPublisher
publisher = MultiAccountTwitterPublisher()
stats = publisher.get_statistics()
print(f'📊 发布统计: {stats}')
"
```

#### 日志监控：
- GitHub Actions 日志：仓库 Actions 页面查看
- 本地日志：`twitter_multi_auto.log` 文件
- 下载日志：Actions 运行页面的 Artifacts

### ⚡ 第九步：快速启动

#### 四账号配置：
1. 在 GitHub Secrets 中添加四个账号的API密钥（共20个密钥）
2. 根据需要调整发布时间
3. 启用定时发布
4. 监控各账号发布效果

### 🆘 故障排除

#### 常见问题：

1. **API密钥配置错误**
   - 检查 GitHub Secrets 名称是否正确
   - 验证四个账号的API密钥是否有效

2. **账号映射不正确**
   - 检查 CSV 文件中"发布账号"字段
   - 确认映射规则是否正确

3. **发布失败**
   - 查看 GitHub Actions 日志
   - 检查 Twitter API 配额
   - 验证账号权限

#### 调试命令：
```bash
# 测试四个账号连接
python connect_twitter_multi.py

# 运行设置向导
python setup_multi_account_matrix.py

# 查看内容统计
python show_content_source.py
```

## 🎉 恭喜！

您的四账号 Twitter 自动发布系统已配置完成！现在可以：

✅ 根据内容类型自动选择四个发布账号  
✅ 定时自动发布，无需人工干预  
✅ 专业的账号矩阵运营策略  
✅ 完整的日志记录和状态追踪  
✅ 灵活的时间安排和批量发布  

开始享受智能化的四账号 Twitter 内容发布体验吧！🚀 