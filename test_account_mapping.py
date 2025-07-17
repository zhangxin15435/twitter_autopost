#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试账号映射逻辑
验证Issue发布工作流中的账号映射是否正确
"""

import logging
from main_multi_account import MultiAccountTwitterPublisher

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def normalize_account_name(account):
    """标准化账号名称，与Issue工作流保持一致"""
    account = account.lower().strip()
    mapping = {
        'contextspace': 'ContextSpace',
        'context space': 'ContextSpace', 
        'twitter': 'ContextSpace',
        'oss discoveries': 'OSS Discoveries',
        'ossdiscoveries': 'OSS Discoveries',
        'oss': 'OSS Discoveries',
        'ai flow watch': 'Ai flow watch',
        'aiflowwatch': 'Ai flow watch', 
        'ai': 'Ai flow watch',
        'open source reader': 'Open source reader',
        'opensourcereader': 'Open source reader',
        'reader': 'Open source reader'
    }
    return mapping.get(account, 'ContextSpace')

def test_account_mapping():
    """测试账号映射逻辑"""
    print("🧪 测试Issue发布账号映射逻辑")
    print("=" * 60)
    
    # 测试案例
    test_cases = [
        # Issue中可能出现的账号名称
        ('ContextSpace', 'ContextSpace'),
        ('OSS Discoveries', 'OSS Discoveries'),
        ('Ai flow watch', 'Ai flow watch'),
        ('Open source reader', 'Open source reader'),
        
        # 小写变体
        ('contextspace', 'ContextSpace'),
        ('oss discoveries', 'OSS Discoveries'),
        ('ai flow watch', 'Ai flow watch'),
        ('open source reader', 'Open source reader'),
        
        # 简写形式
        ('twitter', 'ContextSpace'),
        ('oss', 'OSS Discoveries'),
        ('ai', 'Ai flow watch'),
        ('reader', 'Open source reader'),
        
        # 未知账号
        ('unknown account', 'ContextSpace'),
    ]
    
    print("📋 测试账号映射:")
    for input_account, expected_output in test_cases:
        actual_output = normalize_account_name(input_account)
        status = "✅" if actual_output == expected_output else "❌"
        print(f"   {status} '{input_account}' -> '{actual_output}' (期望: '{expected_output}')")
    
    print("\n" + "=" * 60)
    
    # 测试与main_multi_account.py的兼容性
    print("🔄 测试与发布器的兼容性:")
    publisher = MultiAccountTwitterPublisher()
    
    test_accounts = ['ContextSpace', 'OSS Discoveries', 'Ai flow watch', 'Open source reader']
    
    for account in test_accounts:
        print(f"\n🎯 测试账号: {account}")
        
        # 模拟Issue工作流的账号映射
        mapped_account = normalize_account_name(account)
        print(f"   Issue映射: '{account}' -> '{mapped_account}'")
        
        # 测试发布器是否能识别
        try:
            result = publisher.test_single_account(mapped_account)
            account_key = list(result.keys())[0]
            status = result[account_key]['status']
            
            if status == 'success':
                username = result[account_key]['username']
                print(f"   发布器识别: ✅ 成功 -> @{username}")
            elif status == 'failed':
                print(f"   发布器识别: ⚠️ 连接失败 (配置问题)")
            else:
                error = result[account_key].get('error', '未知错误')
                print(f"   发布器识别: ❌ 错误 - {error}")
                
        except Exception as e:
            print(f"   发布器识别: ❌ 异常 - {str(e)}")
    
    print("\n" + "=" * 60)
    print("✅ 账号映射测试完成")

def test_issue_content_parsing():
    """测试Issue内容解析"""
    print("\n🧪 测试Issue内容解析")
    print("=" * 60)
    
    # 模拟不同的Issue内容格式
    test_contents = [
        {
            'name': '标准格式',
            'content': '**内容:** 这是一条测试推文\n**账号:** OSS Discoveries'
        },
        {
            'name': '小写账号',
            'content': '**内容:** AI技术分享\n**账号:** ai flow watch'
        },
        {
            'name': '简写账号',
            'content': '**内容:** 开源项目推荐\n**账号:** reader'
        },
        {
            'name': '默认账号',
            'content': '**内容:** 默认推文内容'
        }
    ]
    
    import re
    
    def parse_issue_content(content):
        """简化的Issue内容解析"""
        tweets = []
        
        # 解析结构化格式
        pattern = r'\*\*内容:\*\*\s*(.+?)(?:\n\*\*账号:\*\*\s*(.+?))?(?=\n\*\*|$)'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for match in matches:
            tweet_content = match[0].strip()
            account = match[1].strip() if match[1] else 'ContextSpace'
            
            if tweet_content:
                tweets.append({
                    'content': tweet_content,
                    'account': account
                })
        
        return tweets
    
    for test_case in test_contents:
        print(f"\n📝 测试案例: {test_case['name']}")
        print(f"   输入: {test_case['content']}")
        
        tweets = parse_issue_content(test_case['content'])
        
        if tweets:
            for i, tweet in enumerate(tweets):
                original_account = tweet['account']
                mapped_account = normalize_account_name(original_account)
                print(f"   推文{i+1}: '{tweet['content'][:30]}...'")
                print(f"   账号映射: '{original_account}' -> '{mapped_account}'")
        else:
            print("   ❌ 未解析到推文内容")
    
    print("\n" + "=" * 60)
    print("✅ Issue内容解析测试完成")

def main():
    """主函数"""
    print("🚀 启动账号映射和Issue解析测试")
    print("🎯 目的: 验证Issue发布到不同账号的逻辑是否正确")
    print("=" * 80)
    
    test_account_mapping()
    test_issue_content_parsing()
    
    print("\n" + "=" * 80)
    print("🎉 所有测试完成！")
    print("💡 如果测试显示映射正确但Issue发布仍有问题，请检查:")
    print("   1. GitHub Secrets中的API密钥配置")
    print("   2. Issue内容格式是否正确")
    print("   3. GitHub Actions工作流日志")

if __name__ == "__main__":
    main() 