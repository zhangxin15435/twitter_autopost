# 🚀 Twitter自动发布系统

一个基于CSV文件和Twitter API的智能发布工具，支持多账号自动发布，完全不依赖其他平台。

## ✨ 功能特性

- 🐦 **纯Twitter发布**：专注于Twitter平台，无其他平台依赖
- 📊 **CSV数据源**：从CSV文件读取内容，简单易管理
- 🎯 **多账号支持**：智能根据内容类型选择不同Twitter账号发布
- ⏰ **定时自动发布**：GitHub Actions定时任务，无需服务器
- 🔄 **智能内容管理**：自动标记已发布内容，避免重复
- 📝 **推文格式化**：自动格式化内容，符合Twitter字符限制
- 🤖 **完全自动化**：基于GitHub Actions，部署一次永久运行
- 📈 **统计监控**：实时统计发布状态和账号表现

## 🎯 多账号策略

系统支持根据内容类型自动选择发布账号：

| 内容类型 | 目标账号 | 适用场景 |
|---------|---------|---------|
| `ai flow watch` | @AIFlowWatch | AI技术、机器学习 |
| `OpenSource Radar` | @OpenSourceRadar | 开源项目介绍 |
| `oss discoveries` | @OSSDiscoveries | 开源工具发现 |
| `twitter` 或空白 | 主账号 | 综合内容 |

## 🛠️ 技术栈

- **Python 3.11**
- **Twitter API v2**
- **GitHub Actions**
- **Tweepy**
- **CSV文件数据源**

## 📋 前置要求

### 1. Twitter API配置
- 申请Twitter开发者账户
- 为每个账号创建应用获取API密钥
- 需要的密钥：`API Key`、`API Secret`、`Access Token`、`Access Token Secret`、`Bearer Token`

### 2. CSV文件格式
确保您的CSV文件包含以下字段：
- `内容主题` (文本) - 推文内容
- `提出人` (文本) - 作者信息
- `发布账号` (文本) - 目标Twitter账号
- `是否发布` (文本) - 发布状态标记

## 🚀 快速开始

### 方案一：单账号模式（推荐新手）

#### 1. 配置GitHub Secrets
在仓库设置中添加以下密钥：
```
TWITTER_CONSUMER_KEY=你的API密钥
TWITTER_CONSUMER_SECRET=你的API密钥密码
TWITTER_ACCESS_TOKEN=你的访问令牌
TWITTER_ACCESS_TOKEN_SECRET=你的访问令牌密码
TWITTER_BEARER_TOKEN=你的Bearer令牌
```

#### 2. 准备内容文件
将CSV文件放入 `content/` 目录，确保包含必要字段。

#### 3. 测试运行
```bash
# 本地测试
python main.py test

# 单次发布
python main.py run

# 查看状态
python main.py status
```

#### 4. 启用自动发布
推送代码到GitHub，工作流将自动运行。

### 方案二：多账号矩阵（推荐专业用户）

#### 1. 配置多个Twitter账号密钥
```
# 主账号
TWITTER_CONSUMER_KEY=主账号密钥
TWITTER_CONSUMER_SECRET=主账号密钥密码
TWITTER_ACCESS_TOKEN=主账号令牌
TWITTER_ACCESS_TOKEN_SECRET=主账号令牌密码
TWITTER_BEARER_TOKEN=主账号Bearer令牌

# AI Flow Watch账号
TWITTER_AIFLOWWATCH_CONSUMER_KEY=AI账号密钥
TWITTER_AIFLOWWATCH_CONSUMER_SECRET=AI账号密钥密码
TWITTER_AIFLOWWATCH_ACCESS_TOKEN=AI账号令牌
TWITTER_AIFLOWWATCH_ACCESS_TOKEN_SECRET=AI账号令牌密码
TWITTER_AIFLOWWATCH_BEARER_TOKEN=AI账号Bearer令牌

# 其他账号类似配置...
```

#### 2. 运行多账号设置向导
```bash
python setup_multi_account_matrix.py
```

#### 3. 测试多账号配置
```bash
python connect_twitter_multi.py
```

## ⚙️ 配置说明

### 环境变量
创建 `.env` 文件：

```bash
# Twitter API 配置 - 主账号
TWITTER_CONSUMER_KEY=your_twitter_consumer_key
TWITTER_CONSUMER_SECRET=your_twitter_consumer_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
TWITTER_BEARER_TOKEN=your_twitter_bearer_token

# 其他配置
TIMEZONE=Asia/Shanghai
DEBUG=False
```

### GitHub Actions配置
项目包含完整的GitHub Actions工作流：

- `auto_publish_multi_account.yml` - 多账号自动发布
- `schedule_publish.yml` - 定时发布任务
- `manual_publish.yml` - 手动触发发布

## 📊 使用统计

查看详细的使用统计：

```bash
# 查看内容统计
python -c "
from main_multi_account import MultiAccountTwitterPublisher
publisher = MultiAccountTwitterPublisher()
stats = publisher.get_statistics()
print(f'总内容: {stats[\"total\"]}')
print(f'已发布: {stats[\"published\"]}')
print(f'待发布: {stats[\"unpublished\"]}')
"

# 查看账号状态
python -c "
from main_multi_account import MultiAccountTwitterPublisher
publisher = MultiAccountTwitterPublisher()
results = publisher.test_all_accounts()
for account, result in results.items():
    status = '✅' if result['status'] == 'success' else '❌'
    print(f'{status} {account}: @{result.get(\"username\", \"unknown\")}')
"
```

## 🎮 命令说明

### 主程序命令
```bash
python main.py test      # 测试连接和内容
python main.py run       # 执行单次发布
python main.py status    # 查看系统状态
python main.py schedule  # 定时任务模式
```

### 多账号专用命令
```bash
python main_multi_account.py           # 多账号单次发布
python connect_twitter_multi.py        # 测试多账号连接
python setup_multi_account_matrix.py   # 多账号设置向导
```

### 工具命令
```bash
python show_content_source.py          # 显示内容源信息
```

## 🔧 自定义配置

### 修改发布时间
编辑 `.github/workflows/schedule_publish.yml`：

```yaml
schedule:
  # 每天北京时间 6:00, 12:00, 18:00, 24:00
  - cron: '0 22,4,10,16 * * *'
```

### 账号映射规则
修改 `connect_twitter_multi.py` 中的映射规则：

```python
ACCOUNT_MAPPING = {
    'ai flow watch': 'aiflowwatch',
    'OpenSource Radar': 'opensourceradar',
    'oss discoveries': 'ossdiscoveries',
    # 添加你的映射规则
}
```

## 📈 监控和日志

### 查看运行日志
- GitHub Actions日志：仓库Actions页面
- 本地日志：`twitter_multi_auto.log`
- 下载日志：Actions运行页面的Artifacts

### 监控指标
- 发布成功率
- 账号连接状态
- 内容发布分布
- API配额使用情况

## 🆘 故障排除

### 常见问题

1. **API连接失败**
   - 检查GitHub Secrets配置
   - 验证Twitter API密钥有效性
   - 确认账号权限设置

2. **内容获取失败**
   - 检查CSV文件格式
   - 确认content目录存在
   - 验证文件编码格式

3. **发布失败**
   - 检查推文内容长度
   - 验证账号发布权限
   - 查看API配额限制

### 调试技巧
```bash
# 开启调试模式
export DEBUG=True
python main.py test

# 查看详细日志
tail -f twitter_multi_auto.log

# 测试特定功能
python -c "from connect_twitter_multi import TwitterAccountManager; print(TwitterAccountManager().test_all_accounts())"
```

## 🎉 成功案例

- ✅ 支持单账号和多账号模式
- ✅ 完全自动化的GitHub Actions部署
- ✅ 智能内容分发和账号选择
- ✅ 实时状态监控和日志记录

## 📞 获取帮助

1. 查看项目文档和指南
2. 检查GitHub Actions运行日志
3. 运行本地测试命令排查问题
4. 查看示例配置文件

---

**开始使用纯Twitter自动发布系统，告别复杂的多平台依赖！** 🚀 