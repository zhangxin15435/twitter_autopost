# 🚀 Twitter智能多账号自动发布系统

一个功能完整的Twitter多账号智能发布平台，集成前端界面、GitHub Actions自动化工作流和CSV数据管理。

## ✨ 系统特色

🎯 **多账号智能发布**
- 支持4个专业Twitter账号同时管理
- 智能内容分发，根据内容类型自动选择合适账号
- 账号状态管理，可随时启用/禁用特定账号

🖥️ **现代化前端界面**
- 美观的Web控制台，支持直接推文发布
- 响应式设计，完美适配桌面和移动设备
- 实时字符计数，智能推文格式化

🤖 **全自动化工作流**
- GitHub Actions定时发布，无需服务器
- 手动触发发布，支持调试模式
- CSV文件数据源，批量内容管理

📊 **智能数据管理**
- 自动标记已发布内容，避免重复
- 发布状态统计和监控
- 灵活的内容过滤和选择

## 🏢 四个专业账号定位

| 账号 | Twitter用户名 | 内容定位 | 发布策略 |
|------|---------------|----------|----------|
| **ContextSpace** | `@ContextSpace` | 主账号，综合内容发布 | 通用内容、用户增长 |
| **OSS Discoveries** | `@OSSDiscoveries` | 开源工具发现、设计工具 | 开源项目、工具推荐 |
| **AI Flow Watch** | `@AIFlowWatch` | AI技术、机器学习、工作流 | AI资讯、技术分享 |
| **Open Source Reader** | `@OpenSourceReader` | 开源项目介绍、技术评测 | 项目评测、技术深度 |

## 🛠️ 技术架构

### 核心技术栈
- **Python 3.11** - 主要开发语言
- **Twitter API v2** - 官方API接口
- **GitHub Actions** - 自动化CI/CD
- **Tweepy 4.14.0** - Twitter API客户端
- **HTML5/CSS3/JavaScript** - 前端界面

### 系统架构
```
Twitter自动发布系统
├── 前端界面 (index.html)
│   ├── 推文编辑器
│   ├── 账号选择器  
│   └── 一键发布功能
├── 核心引擎
│   ├── 多账号管理 (connect_twitter_multi.py)
│   ├── 发布引擎 (main_multi_account.py)
│   └── 配置管理 (twitter_accounts_config.py)
├── 数据层
│   ├── CSV内容库 (content/)
│   ├── 账号状态 (twitter_accounts_status.json)
│   └── 环境配置 (.env)
└── 自动化层
    ├── 定时发布 (schedule_publish.yml)
    ├── 手动发布 (manual_publish.yml)
    └── 持续集成 (ci.yml)
```

## 🚀 快速开始

### 前置准备

1. **GitHub仓库权限** - 确保能修改仓库设置
2. **Twitter开发者账户** - 为每个账号申请API密钥
3. **内容准备** - 准备要发布的推文内容（CSV格式）

### 第一步：配置GitHub Secrets

在GitHub仓库的 **Settings > Secrets and variables > Actions** 中配置以下密钥：

#### ContextSpace主账号
```
TWITTER_CONTEXTSPACE_CONSUMER_KEY=你的API密钥
TWITTER_CONTEXTSPACE_CONSUMER_SECRET=你的API密钥密码
TWITTER_CONTEXTSPACE_ACCESS_TOKEN=你的访问令牌
TWITTER_CONTEXTSPACE_ACCESS_TOKEN_SECRET=你的访问令牌密码
TWITTER_CONTEXTSPACE_BEARER_TOKEN=你的Bearer令牌
```

#### OSS Discoveries账号
```
TWITTER_OSSDISCOVERIES_CONSUMER_KEY=OSS账号API密钥
TWITTER_OSSDISCOVERIES_CONSUMER_SECRET=OSS账号API密钥密码
TWITTER_OSSDISCOVERIES_ACCESS_TOKEN=OSS账号访问令牌
TWITTER_OSSDISCOVERIES_ACCESS_TOKEN_SECRET=OSS账号访问令牌密码
TWITTER_OSSDISCOVERIES_BEARER_TOKEN=OSS账号Bearer令牌
```

#### AI Flow Watch账号
```
TWITTER_AIFLOWWATCH_CONSUMER_KEY=AI账号API密钥
TWITTER_AIFLOWWATCH_CONSUMER_SECRET=AI账号API密钥密码
TWITTER_AIFLOWWATCH_ACCESS_TOKEN=AI账号访问令牌
TWITTER_AIFLOWWATCH_ACCESS_TOKEN_SECRET=AI账号访问令牌密码
TWITTER_AIFLOWWATCH_BEARER_TOKEN=AI账号Bearer令牌
```

#### Open Source Reader账号
```
TWITTER_OPENSOURCEREADER_CONSUMER_KEY=Reader账号API密钥
TWITTER_OPENSOURCEREADER_CONSUMER_SECRET=Reader账号API密钥密码
TWITTER_OPENSOURCEREADER_ACCESS_TOKEN=Reader账号访问令牌
TWITTER_OPENSOURCEREADER_ACCESS_TOKEN_SECRET=Reader账号访问令牌密码
TWITTER_OPENSOURCEREADER_BEARER_TOKEN=Reader账号Bearer令牌
```

### 第二步：准备内容文件

在 `content/` 目录下创建CSV文件，包含以下字段：
- **内容主题** - 推文正文内容
- **提出人** - 内容作者（可选）
- **发布账号** - 目标账号标识
- **是否发布** - 发布状态标记

#### 账号标识映射
| CSV中的标识 | 对应账号 |
|-------------|----------|
| `contextspace` 或 `twitter` | ContextSpace主账号 |
| `oss discoveries` | OSS Discoveries |
| `ai flow watch` | AI Flow Watch |
| `opensourcereader` | Open Source Reader |

### 第三步：测试连接

```bash
# 克隆项目到本地
git clone [你的仓库地址]
cd twitter_autopost

# 安装依赖
pip install -r requirements.txt

# 创建本地环境文件（参考config.env.example）
cp config.env.example .env
# 编辑.env文件，填入你的API密钥

# 测试所有账号连接
python connect_twitter_multi.py

# 查看账号状态
python manage_accounts.py --status
```

### 第四步：启用自动发布

推送代码到GitHub，系统将自动启用：
- **定时发布** - 每天指定时间自动发布
- **手动发布** - 支持通过前端界面或GitHub Actions手动触发

## 📱 使用方法

### 方式一：Issue发布（推荐，任何人都可使用）

1. **打开控制台**
   - 在浏览器中打开 `index.html`
   - 切换到"🎫 Issue发布"标签页

2. **编写推文**
   - 在文本框中输入推文内容
   - 系统实时显示字符计数（最多280字符）
   - 选择目标发布账号

3. **创建Issue**
   - 点击"🎫 创建Issue发布推文"
   - 自动跳转到GitHub Issue创建页面
   - 标题和内容已自动填充

4. **提交发布**
   - 点击"Submit new issue"提交
   - 系统自动解析并发布推文
   - 发布结果会在Issue中自动回复

### 方式二：前端界面发布（需要仓库权限）

1. **打开控制台**
   - 在浏览器中打开 `index.html`
   - 选择"📝 单条推文"标签页

2. **编写推文**
   - 在文本框中输入推文内容
   - 系统实时显示字符计数（最多280字符）
   - 支持多行文本和特殊字符

3. **选择账号**
   - 点击选择目标发布账号
   - 每个账号有明确的定位说明

4. **发布推文**
   - 点击"🚀 立即发布推文"
   - 内容自动复制到剪贴板
   - 跳转到GitHub Actions发布页面

### 方式三：CSV批量发布（需要仓库权限）

1. **准备内容**
   ```csv
   内容主题,提出人,发布账号,是否发布
   "这是一个很棒的AI工具！#AI #工具","张三","ai flow watch","否"
   "推荐一个开源项目，值得关注","李四","oss discoveries","否"
   ```

2. **上传文件**
   - 将CSV文件放入 `content/` 目录
   - 推送到GitHub触发自动发布

3. **监控发布**
   - 在GitHub Actions页面查看发布状态
   - 系统自动更新"是否发布"字段

### 方式四：直接创建GitHub Issue

**适用于任何人，无需仓库权限！**

1. **访问Issue页面**
   ```
   https://github.com/zhangxin15435/twitter_autopost/issues/new?template=tweet_publish.md
   ```

2. **填写Issue内容**
   使用以下格式：
   ```
   **内容:** 这里填写推文内容
   **账号:** ContextSpace
   ```

3. **提交Issue**
   - 确保标题包含`[推文发布]`
   - 点击"Submit new issue"
   - 系统自动处理并发布

4. **查看结果**
   - 发布完成后Issue中会自动回复结果
   - 成功的Issue会添加`published`标签

### 方式五：命令行发布

```bash
# 单次发布
python main_multi_account.py

# 指定内容发布
python main.py run

# 查看统计信息
python main.py status

# 测试模式（不实际发布）
python main.py test
```

## ⚙️ 高级配置

### 账号管理

```bash
# 查看所有账号状态
python manage_accounts.py --status

# 启用特定账号
python manage_accounts.py --enable contextspace

# 禁用特定账号
python manage_accounts.py --disable aiflowwatch

# 测试账号连接
python manage_accounts.py --test ossdiscoveries
```

### 定时发布设置

编辑 `.github/workflows/schedule_publish.yml` 修改发布时间：

```yaml
schedule:
  # 每天北京时间 9:00, 15:00, 21:00
  - cron: '0 1,7,13 * * *'
```

### 内容过滤规则

在 `main_multi_account.py` 中自定义过滤逻辑：

```python
def should_publish_content(self, content: str, account: str) -> bool:
    """自定义发布规则"""
    # 添加你的自定义逻辑
    if len(content) < 10:  # 太短的内容不发布
        return False
    
    if '测试' in content:  # 包含测试字样的不发布
        return False
        
    return True
```

## 📊 监控和统计

### 发布统计

```bash
# 查看总体统计
python -c "
from main_multi_account import MultiAccountTwitterPublisher
publisher = MultiAccountTwitterPublisher()
stats = publisher.get_statistics()
print(f'总内容数: {stats[\"total\"]}')
print(f'已发布: {stats[\"published\"]}')
print(f'待发布: {stats[\"unpublished\"]}')
"

# 查看各账号状态
python -c "
from connect_twitter_multi import TwitterAccountManager
manager = TwitterAccountManager()
results = manager.test_all_accounts()
for account, result in results.items():
    status = '✅' if result['status'] == 'success' else '❌'
    print(f'{status} {account}: @{result.get(\"username\", \"unknown\")}')
"
```

### 日志查看

- **GitHub Actions日志**: 仓库Actions页面查看详细运行日志
- **本地日志**: `twitter_multi_auto.log` 文件
- **错误排查**: 工作流失败时可下载日志文件分析

## 🛠️ 故障排除

### 常见问题

#### 1. API连接失败
**错误信息**: `Twitter API配置不完整`

**解决方案**:
- 检查GitHub Secrets是否正确配置
- 验证Twitter API密钥有效性
- 确认账号权限和应用设置

#### 2. 内容发布失败
**错误信息**: `推文发布失败`

**解决方案**:
- 检查推文内容长度（最多280字符）
- 验证账号是否有发布权限
- 查看是否触发了Twitter的反垃圾机制

#### 3. CSV文件读取错误
**错误信息**: `读取content文件失败`

**解决方案**:
- 确认CSV文件格式正确
- 检查文件编码（推荐UTF-8）
- 验证必要字段是否存在

#### 4. 账号暂时禁用
**错误信息**: `账号已禁用或配置未找到`

**解决方案**:
```bash
# 检查账号状态
python manage_accounts.py --status

# 启用特定账号
python manage_accounts.py --enable [账号名]
```

### 调试模式

```bash
# 启用详细日志
export DEBUG=True
python main_multi_account.py

# 测试特定功能
python connect_twitter_multi.py

# 验证配置完整性
python -c "from twitter_accounts_config import TwitterAccountsConfig; print('配置检查:', TwitterAccountsConfig().validate_all_configs())"
```

## 📁 项目文件结构

```
twitter_autopost/
├── 📊 核心程序
│   ├── main.py                          # 单账号主程序
│   ├── main_multi_account.py            # 多账号发布引擎
│   ├── connect_twitter_multi.py         # 多账号API连接管理
│   ├── twitter_accounts_config.py       # 账号配置管理
│   └── manage_accounts.py               # 账号状态管理工具
├── 🎮 用户界面
│   ├── index.html                       # 前端发布控制台
│   └── manual_publish.py               # 手动发布脚本
├── 📋 配置文件
│   ├── requirements.txt                 # Python依赖
│   ├── config.env.example               # 环境变量模板
│   ├── twitter_accounts_status.json     # 账号启用状态
│   └── .gitignore                       # Git忽略规则
├── 📂 数据目录
│   └── content/                         # CSV内容文件目录
│       └── *.csv                        # 发布内容数据
├── 🤖 自动化工作流
│   └── .github/
│       ├── workflows/
│       │   ├── manual_publish.yml       # 手动发布工作流
│       │   ├── schedule_publish.yml     # 定时发布工作流
│       │   ├── issue_trigger_publish.yml # Issue触发发布工作流（推荐）
│       │   └── ci.yml                   # 持续集成工作流
│       └── ISSUE_TEMPLATE/
│           └── tweet_publish.md         # Issue发布模板
└── 📖 文档
    ├── README.md                        # 主要文档（本文件）
    ├── ISSUE_PUBLISH_GUIDE.md           # Issue发布详细指南
    └── PROJECT_CLEANUP_SUMMARY.md       # 项目清理总结文档
```

## 🔄 更新日志

### v2.0.0 (当前版本)
- ✅ 完整的四账号多发布系统
- ✅ 现代化前端界面
- ✅ GitHub Actions自动化工作流
- ✅ 智能内容分发和账号选择
- ✅ 完善的错误处理和日志记录
- ✅ 账号状态动态管理
- ✅ 性能优化和缓存机制

### 已解决的问题
- ✅ 依赖包缺失问题
- ✅ 账号配置验证
- ✅ GitHub Actions工作流格式
- ✅ 性能优化（3-5倍速度提升）
- ✅ 错误处理和故障恢复

## 🎯 最佳实践

### 内容策略
1. **账号定位明确** - 根据内容类型选择合适账号
2. **发布时间优化** - 考虑目标受众的活跃时间
3. **内容质量控制** - 使用测试模式验证内容
4. **避免重复发布** - 系统自动标记已发布内容

### 系统维护
1. **定期检查API配额** - 监控Twitter API使用情况
2. **备份重要数据** - 定期备份CSV文件和配置
3. **监控发布状态** - 及时处理失败的发布任务
4. **更新依赖包** - 保持系统安全和稳定

### 安全建议
1. **保护API密钥** - 仅在GitHub Secrets中存储
2. **限制访问权限** - 合理配置仓库权限
3. **监控异常活动** - 关注非预期的发布行为

## 📞 技术支持

- 🎫 **Issue发布**: [创建推文发布请求](https://github.com/zhangxin15435/twitter_autopost/issues/new?template=tweet_publish.md)
- 📋 **项目文档**: 查看详细的功能文档和指南
- 🔍 **GitHub Issues**: [提交问题和功能建议](https://github.com/zhangxin15435/twitter_autopost/issues)
- 📊 **GitHub Actions**: [查看自动化工作流日志](https://github.com/zhangxin15435/twitter_autopost/actions)
- 🧪 **本地测试**: 使用测试命令排查问题

---

**开始使用Twitter智能多账号自动发布系统，让内容发布更高效、更智能！** 🚀

> 💡 **小贴士**: 首次使用建议先在测试模式下熟悉系统，确认一切正常后再启用自动发布。 