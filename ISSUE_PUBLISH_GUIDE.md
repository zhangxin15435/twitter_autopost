# 🎫 Issue发布使用指南

## 📖 概述

Issue发布是我们的**推荐发布方式**，因为它允许**任何人**无需仓库权限即可发布推文到我们的多个Twitter账号。

## ✨ 为什么选择Issue发布？

### 🔓 **完全开放**
- 无需GitHub仓库协作者权限
- 任何人都可以创建Issue
- 完全公开透明的发布流程

### 🤖 **全自动化**
- 创建Issue后自动触发发布
- 自动解析推文内容和目标账号
- 发布结果自动回复到Issue

### 📝 **完整记录**
- 每个发布请求都有完整的Issue记录
- 可以查看历史发布内容
- 便于追踪和管理

## 🚀 快速开始

### 方式一：通过前端界面（推荐）

1. **打开发布控制台**
   ```
   https://[你的域名]/index.html
   ```

2. **切换到Issue发布标签页**
   - 点击"🎫 Issue发布"标签

3. **填写推文内容**
   - 输入推文内容（最多280字符）
   - 选择目标Twitter账号

4. **创建Issue**
   - 点击"🎫 创建Issue发布推文"
   - 自动跳转到GitHub Issue页面
   - 标题和内容已自动填充

5. **提交发布**
   - 点击"Submit new issue"
   - 等待自动发布（通常1-2分钟）
   - 查看Issue中的发布结果

### 方式二：直接创建GitHub Issue

1. **访问Issue模板页面**
   ```
   https://github.com/zhangxin15435/twitter_autopost/issues/new?template=tweet_publish.md
   ```

2. **填写Issue内容**
   删除模板中的说明文字，按以下格式填写：

   #### 单条推文格式：
   ```
   **内容:** 这里填写推文内容（最多280字符）
   **账号:** ContextSpace
   ```

   #### 多条推文格式：
   ```
   **内容:** 第一条推文内容
   **账号:** ContextSpace

   ---

   **内容:** 第二条推文内容
   **账号:** AI Flow Watch

   ---

   **内容:** 第三条推文内容
   **账号:** OSS Discoveries
   ```

   #### JSON批量格式：
   ```json
   [
     {
       "content": "第一条推文内容",
       "account": "ContextSpace"
     },
     {
       "content": "第二条推文内容", 
       "account": "AI Flow Watch"
     }
   ]
   ```

3. **确认标题格式**
   - 标题必须包含`[推文发布]`
   - 例如：`[推文发布] 分享一个很棒的AI工具`

4. **提交Issue**
   - 点击"Submit new issue"
   - 系统自动开始处理

## 🎯 支持的Twitter账号

| 账号标识 | Twitter用户名 | 内容定位 |
|----------|---------------|----------|
| **ContextSpace** | @ContextSpace | 主账号，综合内容发布 |
| **OSS Discoveries** | @OSSDiscoveries | 开源工具发现、设计工具 |
| **AI Flow Watch** | @AIFlowWatch | AI技术、机器学习、工作流 |
| **Open Source Reader** | @OpenSourceReader | 开源项目介绍、技术评测 |

### 账号名称别名

系统支持多种账号名称写法：

- **ContextSpace**: `ContextSpace`, `context space`, `twitter`
- **OSS Discoveries**: `OSS Discoveries`, `ossdiscoveries`, `oss`
- **AI Flow Watch**: `AI Flow Watch`, `Ai flow watch`, `aiflowwatch`, `ai`
- **Open Source Reader**: `Open source reader`, `opensourcereader`, `reader`

## ⚡ 自动化流程

### 1. Issue创建后
- 系统检测标题包含`[推文发布]`
- 自动触发GitHub Actions工作流
- 添加`pending`标签

### 2. 内容解析
- 智能解析Issue内容
- 支持多种格式（文本、JSON）
- 验证推文长度和格式

### 3. 推文发布
- 连接对应的Twitter账号
- 发布推文到指定账号
- 记录发布结果

### 4. 结果反馈
- 在Issue中自动回复发布结果
- 成功：添加`published`标签
- 失败：添加`failed`标签

## 📋 注意事项

### ✅ 最佳实践

1. **内容质量**
   - 确保推文内容有价值
   - 遵守Twitter社区准则
   - 避免重复或垃圾内容

2. **格式规范**
   - 严格按照模板格式填写
   - 不要修改自动生成的说明部分
   - 确保标题包含`[推文发布]`

3. **账号选择**
   - 根据内容类型选择合适的账号
   - 参考各账号的定位说明

### ⚠️ 使用限制

1. **字符限制**
   - 单条推文不超过280字符
   - 系统会自动截断超长内容

2. **频率限制**
   - 避免短时间内大量发布
   - 建议合理控制发布频率

3. **内容审核**
   - 所有内容都是公开可见的
   - 请确保内容符合相关规定

## 🔍 故障排除

### 常见问题

#### Q: Issue创建后没有自动发布？
**A**: 检查以下几点：
- 标题是否包含`[推文发布]`
- Issue内容格式是否正确
- 查看GitHub Actions是否正常运行

#### Q: 发布失败怎么办？
**A**: 常见原因：
- 推文内容超过280字符
- 账号API配额已满
- 网络连接问题
- 内容格式错误

#### Q: 如何查看发布状态？
**A**: 
- 查看Issue中的自动回复
- 检查Issue标签（`published`/`failed`）
- 查看GitHub Actions运行日志

#### Q: 可以删除或修改已创建的Issue吗？
**A**: 
- Issue创建后会立即触发发布
- 建议不要修改正在处理的Issue
- 如需修改，请创建新的Issue

## 📞 获取帮助

- 🎫 **创建发布Issue**: [点击这里](https://github.com/zhangxin15435/twitter_autopost/issues/new?template=tweet_publish.md)
- 🔍 **查看历史Issues**: [点击这里](https://github.com/zhangxin15435/twitter_autopost/issues)
- 📊 **查看工作流状态**: [点击这里](https://github.com/zhangxin15435/twitter_autopost/actions)
- 📖 **完整文档**: [README.md](./README.md)

---

**开始使用Issue发布功能，让推文发布变得更简单！** 🚀 