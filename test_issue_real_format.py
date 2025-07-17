#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试真实Issue格式的内容解析
重现用户报告的发布不完整问题
"""

import re
import json

def parse_issue_content_exact(content):
    """与工作流完全相同的解析逻辑"""
    tweets = []
    
    print(f"🔍 原始内容长度: {len(content)} 字符")
    print(f"📝 原始内容:")
    print("=" * 60)
    print(repr(content))
    print("=" * 60)
    
    # 方法1：JSON格式
    json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
    if json_match:
        try:
            data = json.loads(json_match.group(1))
            if isinstance(data, list):
                tweets.extend(data)
            else:
                tweets.append(data)
            print("✅ 找到JSON格式内容")
            return tweets
        except:
            print("❌ JSON格式解析失败")
            pass
    
    # 方法2：结构化文本格式
    lines = content.split('\n')
    current_tweet = {}
    
    print(f"📄 总行数: {len(lines)}")
    
    for i, line in enumerate(lines):
        line = line.strip()
        print(f"第{i+1}行: {repr(line)}")
        
        if line.startswith('**内容:**') or line.startswith('内容:'):
            content_text = line.split(':', 1)[1].strip()
            # 清理可能的星号
            content_text = content_text.lstrip('*').strip()
            current_tweet['content'] = content_text
            print(f"  → 找到内容: {repr(content_text)}")
        elif line.startswith('**账号:**') or line.startswith('账号:'):
            account_text = line.split(':', 1)[1].strip()
            # 清理可能的星号
            account_text = account_text.lstrip('*').strip()
            current_tweet['account'] = account_text
            print(f"  → 找到账号: {repr(account_text)}")
        elif line.startswith('---') and current_tweet:
            tweets.append(current_tweet)
            print(f"  → 添加推文: {current_tweet}")
            current_tweet = {}
    
    # 添加最后一条推文
    if current_tweet.get('content'):
        tweets.append(current_tweet)
        print(f"→ 添加最后推文: {current_tweet}")
    
    # 方法3：简单格式（如果没有找到结构化内容）
    if not tweets:
        print("\n🔄 尝试简单格式解析...")
        
        # 查找可能的推文内容
        content_lines = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
        
        print(f"📋 过滤后的内容行数: {len(content_lines)}")
        for i, line in enumerate(content_lines):
            print(f"  内容行{i+1}: {repr(line)}")
        
        if content_lines:
            # 取所有内容，但检查长度限制
            full_content = '\n'.join(content_lines)
            print(f"\n📝 合并后的完整内容长度: {len(full_content)}")
            print(f"📝 合并后的完整内容:")
            print("=" * 60)
            print(repr(full_content))
            print("=" * 60)
            
            # 如果内容超过280字符，截断并添加提示
            if len(full_content) > 280:
                truncated_content = full_content[:270] + "...[内容过长已截断]"
                print(f"⚠️ 内容超长({len(full_content)}字符)，已截断为: {truncated_content}")
                tweets.append({
                    'content': truncated_content,
                    'account': 'ContextSpace'  # 默认账号
                })
            else:
                tweets.append({
                    'content': full_content,
                    'account': 'ContextSpace'  # 默认账号
                })
    
    print("\n🎯 最终解析结果:")
    print(f"  推文数量: {len(tweets)}")
    for i, tweet in enumerate(tweets):
        content_text = tweet.get('content', '')
        print(f"  推文{i+1}:")
        print(f"    账号: {tweet.get('account', 'N/A')}")
        print(f"    内容长度: {len(content_text)} 字符")
        print(f"    内容: {repr(content_text)}")
    
    return tweets

def test_github_issue_markdown_format():
    """测试GitHub Issue中包含Markdown标题的格式"""
    print("🧪 测试: GitHub Issue包含Markdown标题的情况")
    print("=" * 80)
    
    # 模拟用户在GitHub Issue模板中直接写内容的情况
    test_content = """## 📝 推文内容

常见的提供免费代理的网站：
https://www.freeproxylists.net
https://www.hidemyass.com
https://www.proxyscrape.com
http://spys.one
https://www.sslproxies.org
https://www.kproxy.com
https://whoer.net

## 🤖 自动发布说明

此Issue会自动触发推文发布流程：
- 系统会解析上述内容并发布到指定的Twitter账号

发布时间: 2024-01-17 10:30:00"""
    
    result = parse_issue_content_exact(test_content)
    return result

def test_clean_format():
    """测试纯净的多行内容"""
    print("\n🧪 测试: 纯净的多行内容")
    print("=" * 80)
    
    test_content = """常见的提供免费代理的网站：
https://www.freeproxylists.net
https://www.hidemyass.com
https://www.proxyscrape.com
http://spys.one
https://www.sslproxies.org
https://www.kproxy.com
https://whoer.net"""
    
    result = parse_issue_content_exact(test_content)
    return result

def test_structured_format():
    """测试结构化格式"""
    print("\n🧪 测试: 结构化格式")
    print("=" * 80)
    
    test_content = """**内容:** 常见的提供免费代理的网站：
https://www.freeproxylists.net
https://www.hidemyass.com
https://www.proxyscrape.com
http://spys.one
https://www.sslproxies.org
https://www.kproxy.com
https://whoer.net
**账号:** ContextSpace"""
    
    result = parse_issue_content_exact(test_content)
    return result

def test_mixed_content():
    """测试包含其他内容的混合格式"""
    print("\n🧪 测试: 包含其他内容的混合格式")
    print("=" * 80)
    
    test_content = """# 推文发布请求

我要发布以下内容：

常见的提供免费代理的网站：
https://www.freeproxylists.net
https://www.hidemyass.com
https://www.proxyscrape.com
http://spys.one
https://www.sslproxies.org
https://www.kproxy.com
https://whoer.net

请发布到ContextSpace账号。

谢谢！"""
    
    result = parse_issue_content_exact(test_content)
    return result

if __name__ == "__main__":
    print("🔍 GitHub Issue真实格式内容解析测试")
    print("=" * 80)
    
    # 运行所有测试
    results = []
    results.append(test_github_issue_markdown_format())
    results.append(test_clean_format())
    results.append(test_structured_format())
    results.append(test_mixed_content())
    
    print("\n📊 测试总结:")
    print("=" * 80)
    for i, result in enumerate(results, 1):
        if result and len(result) > 0:
            content = result[0].get('content', '')
            length = len(content)
            print(f"测试{i}: 解析成功 - {length}字符")
            if length < 100:  # 如果内容太短，可能是问题
                print(f"  ⚠️  内容可能不完整: {repr(content[:50])}")
            else:
                print(f"  ✅ 内容完整: {repr(content[:50])}...")
        else:
            print(f"测试{i}: ❌ 解析失败")
    
    print("\n✅ 测试完成") 