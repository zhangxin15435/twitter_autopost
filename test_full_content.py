#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试完整内容解析
验证用户输入的所有内容都被正确发布
"""

def test_full_content_parsing():
    """测试完整内容解析"""
    
    # 模拟用户的Issue内容
    user_content = """常见的提供免费代理的网站：
https://www.freeproxylists.net
https://www.hidemyass.com
https://www.proxyscrape.com
http://spys.one
https://www.sslproxies.org
https://www.kproxy.com
https://whoer.net"""
    
    print("🧪 测试完整内容解析")
    print("=" * 60)
    print(f"用户输入内容:")
    print(user_content)
    print("=" * 60)
    
    # 模拟Issue工作流的解析逻辑
    lines = user_content.split('\n')
    tweets = []
    current_tweet = {}
    
    # 检查是否是结构化格式
    has_structured_content = False
    for line in lines:
        line = line.strip()
        if line.startswith('**内容:**') or line.startswith('**账号:**'):
            has_structured_content = True
            break
    
    print(f"📋 结构化格式检测: {'是' if has_structured_content else '否'}")
    
    if not has_structured_content:
        print("🔍 使用简单格式解析")
        
        # 简单格式解析
        content_lines = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
        if content_lines:
            # 取所有内容
            full_content = '\n'.join(content_lines)
            
            print(f"📏 内容长度: {len(full_content)} 字符")
            print(f"📝 完整内容:")
            print(full_content)
            print("-" * 40)
            
            # 检查长度限制
            if len(full_content) > 280:
                truncated_content = full_content[:270] + "...[内容过长已截断]"
                print(f"⚠️ 内容超长，截断为:")
                print(truncated_content)
                tweets.append({
                    'content': truncated_content,
                    'account': 'ContextSpace'
                })
            else:
                print(f"✅ 内容长度符合要求")
                tweets.append({
                    'content': full_content,
                    'account': 'ContextSpace'
                })
    
    print("\n" + "=" * 60)
    print(f"📊 解析结果: {len(tweets)} 条推文")
    
    for i, tweet in enumerate(tweets):
        print(f"\n推文 {i+1}:")
        print(f"  内容长度: {len(tweet['content'])} 字符")
        print(f"  目标账号: {tweet['account']}")
        print(f"  内容预览: {tweet['content'][:100]}...")
        
        if len(tweet['content']) <= 280:
            print(f"  ✅ 长度检查: 符合Twitter限制")
        else:
            print(f"  ❌ 长度检查: 超过280字符限制")

def test_before_after_comparison():
    """对比修复前后的效果"""
    print("\n" + "=" * 80)
    print("🔄 修复前后对比")
    print("=" * 80)
    
    user_content = """常见的提供免费代理的网站：
https://www.freeproxylists.net
https://www.hidemyass.com
https://www.proxyscrape.com
http://spys.one
https://www.sslproxies.org
https://www.kproxy.com
https://whoer.net"""
    
    lines = user_content.split('\n')
    content_lines = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
    
    # 修复前的逻辑（只取前3行）
    before_content = '\n'.join(content_lines[:3])
    
    # 修复后的逻辑（取所有内容）
    after_content = '\n'.join(content_lines)
    
    print("📋 修复前（只取前3行）:")
    print(f"内容: {before_content}")
    print(f"长度: {len(before_content)} 字符")
    
    print("\n📋 修复后（取所有内容）:")
    print(f"内容: {after_content}")
    print(f"长度: {len(after_content)} 字符")
    
    print(f"\n✅ 修复效果: 从 {len(before_content)} 字符增加到 {len(after_content)} 字符")
    print(f"📈 内容完整性: {len(after_content)/len(before_content)*100:.1f}%")

if __name__ == "__main__":
    test_full_content_parsing()
    test_before_after_comparison() 