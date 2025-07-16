---
name: 🐦 推文发布请求
about: 通过Issue发布推文到Twitter多账号
title: '[推文发布] '
labels: ['pending']
assignees: ''

---

## 📝 推文内容

请按照以下格式填写要发布的推文：

### 方式一：结构化格式（推荐）

```
**内容:** 这里填写推文内容（最多280字符）
**账号:** ContextSpace

---

**内容:** 另一条推文的内容
**账号:** AI Flow Watch

---

**内容:** 第三条推文的内容  
**账号:** OSS Discoveries
```

### 方式二：JSON格式（批量发布）

```json
[
  {
    "content": "这是第一条推文内容",
    "account": "ContextSpace"
  },
  {
    "content": "这是第二条推文内容",
    "account": "AI Flow Watch"
  }
]
```

### 方式三：简单格式

直接写推文内容，系统会自动发布到ContextSpace主账号：

```
这里直接写推文内容
可以多行
系统会自动发布
```

## 🎯 支持的账号

- **ContextSpace** - 主账号，综合内容发布
- **OSS Discoveries** - 开源工具发现、设计工具  
- **AI Flow Watch** - AI技术、机器学习、工作流
- **Open Source Reader** - 开源项目介绍、技术评测

## ⚡ 自动化说明

- 创建Issue后，系统会自动解析内容并发布推文
- 发布完成后会在此Issue中回复结果
- 成功发布的Issue会添加`published`标签
- 失败的Issue会添加`failed`标签

## 📋 注意事项

1. Issue标题必须包含`[推文发布]`才会触发自动发布
2. 推文内容不能超过280字符
3. 请确保内容符合Twitter社区准则
4. 系统会自动去除多余的空格和换行

---

**开始编辑上方内容，删除这些说明文字，然后提交Issue即可自动发布！** 🚀 