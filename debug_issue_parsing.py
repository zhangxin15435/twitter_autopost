#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试Issue内容解析问题
测试不同格式的内容解析结果
"""

import re
import json

def parse_issue_content(content):
    """解析Issue内容，提取推文数据（与工作流中相同的逻辑）"""
    tweets = []
    
    print(f"🔍 原始内容长度: {len(content)} 字符")
    print(f"📝 原始内容:\n{repr(content)}")
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
        print("🔄 尝试简单格式解析...")
        
        # 查找可能的推文内容
        content_lines = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
        
        print(f"📋 过滤后的内容行数: {len(content_lines)}")
        for i, line in enumerate(content_lines):
            print(f"  内容行{i+1}: {repr(line)}")
        
        if content_lines:
            # 取所有内容，但检查长度限制
            full_content = '\n'.join(content_lines)
            print(f"📝 合并后的完整内容长度: {len(full_content)}")
            print(f"📝 合并后的完整内容: {repr(full_content)}")
            
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
    
    print("=" * 60)
    print(f"🎯 最终解析结果: {len(tweets)} 条推文")
    for i, tweet in enumerate(tweets):
        print(f"  推文{i+1}: 内容长度={len(tweet.get('content', ''))} 字符")
        print(f"         账号={tweet.get('account', 'N/A')}")
        print(f"         内容前50字符: {repr(tweet.get('content', '')[:50])}")
    
    return tweets

def test_multi_line_content():
    """测试多行内容解析"""
    print("🧪 测试1: 多行列表内容")
    print("=" * 80)
    
    test_content = """常见的提供免费代理的网站：
https://www.freeproxylists.net
https://www.hidemyass.com
https://www.proxyscrape.com
http://spys.one
https://www.sslproxies.org
https://www.kproxy.com
https://whoer.net"""
    
    result = parse_issue_content(test_content)
    
    print("\n🧪 测试2: 带结构化格式的内容")
    print("=" * 80)
    
    test_content2 = """**内容:** 常见的提供免费代理的网站：
https://www.freeproxylists.net
https://www.hidemyass.com
https://www.proxyscrape.com
**账号:** ContextSpace"""
    
    result2 = parse_issue_content(test_content2)

def test_actual_issue_content():
    """测试实际Issue内容"""
    print("🧪 测试3: 模拟实际Issue内容")
    print("=" * 80)
    
    # 模拟GitHub Issue的实际内容格式
    test_content3 = """## 📝 推文内容

常见的提供免费代理的网站：
https://www.freeproxylists.net
https://www.hidemyass.com
https://www.proxyscrape.com
http://spys.one
https://www.sslproxies.org
https://www.kproxy.com
https://whoer.net

## 其他信息

发布时间: 2024-01-01"""
    
    result3 = parse_issue_content(test_content3)

if __name__ == "__main__":
    print("🔍 Issue内容解析调试器")
    print("=" * 80)
    
    test_multi_line_content()
    test_actual_issue_content()
    
    print("\n✅ 调试完成") 