# 🐦 Twitter手动发布系统使用指南

## 📖 系统介绍

这是一个功能完整的Twitter四账号手动发布系统，包含前端控制台和GitHub Actions自动化工作流。

## 🎯 主要功能

- ✨ 现代化前端界面，支持直接输入推文内容
- 🎨 四账号智能选择，每个账号都有专门的定位
- 📱 响应式设计，完美支持桌面和移动设备
- 🚀 一键发布，直接触发GitHub Actions工作流
- 🐛 调试模式，可预览不实际发布

## 🏢 四个专业账号

1. **🏢 ContextSpace**: 主账号，综合内容发布
2. **🔧 OSS Discoveries**: 开源工具发现、设计工具
3. **🤖 AI Flow Watch**: AI技术、机器学习、工作流  
4. **📚 Open Source Reader**: 开源项目介绍、技术评测

## 🎮 使用方法

### 方式一：前端控制台（推荐）

1. **打开前端页面**
   - 在浏览器中打开 `index.html`
   - 界面会显示Twitter发布控制台

2. **输入推文内容**
   - 在文本框中输入要发布的推文
   - 实时显示字符计数（最多280字符）
   - 接近限制时显示警告颜色

3. **选择目标账号**
   - 点击选择要发布到的账号
   - 每个账号都有清晰的说明和定位

4. **一键发布**
   - 点击"🚀 立即发布推文"
   - 内容会自动复制到剪贴板
   - 自动跳转到GitHub Actions页面

### 方式二：GitHub Actions直接发布

1. **访问GitHub Actions**
   ```
   https://github.com/zhangxin15435/twitter_autopost/actions/workflows/manual_publish.yml
   ```

2. **点击 "Run workflow"**

3. **填写发布信息**
   - 推文内容：输入要发布的内容
   - 选择发布账号：从下拉菜单选择
   - 调试模式：可选（仅预览不发布）

4. **执行发布**
   - 点击绿色的"Run workflow"按钮
   - 等待执行完成，查看结果

## 🔧 技术特性

### 前端特性
- 实时字符计数和验证
- 响应式设计适配所有设备
- 自动保存防止内容丢失
- 剪贴板自动复制功能

### 后端特性  
- Python脚本处理发布逻辑
- 多层验证确保内容有效性
- 完整的日志记录和错误处理
- 支持调试模式测试

## 🚀 快速开始

1. **确保配置完成**
   - 四个账号的Twitter API密钥已配置
   - GitHub Actions权限设置正确

2. **测试发布**
   ```
   内容：Hello from Twitter发布控制台! 🚀
   账号：ContextSpace
   模式：调试模式（测试用）
   ```

3. **正式发布**
   - 关闭调试模式
   - 输入真实要发布的内容
   - 选择合适的账号并发布

## 📊 文件说明

- `index.html` - 前端发布控制台
- `manual_publish.py` - 手动发布Python脚本
- `.github/workflows/manual_publish.yml` - GitHub Actions工作流
- `MANUAL_PUBLISH_GUIDE.md` - 本使用指南

## 🛠️ 故障排除

### 常见问题

1. **字符超限**: 推文内容不能超过280字符
2. **账号无效**: 必须选择四个预定义账号之一  
3. **API失败**: 检查Twitter API密钥配置

### 调试方法

1. 先使用调试模式测试
2. 查看GitHub Actions执行日志
3. 验证API密钥和网络连接

---

**✅ 现在您可以轻松地手动发布推文到四个专业Twitter账号了！** 