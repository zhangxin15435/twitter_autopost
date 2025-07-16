#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试账号映射问题的调试脚本
模拟GitHub Actions环境
"""

import os
import sys

# 模拟GitHub Actions中的环境变量
def setup_test_env():
    """设置测试环境变量"""
    print("🧪 设置测试环境变量...")
    
    # ContextSpace主账号
    os.environ['TWITTER_CONTEXTSPACE_CONSUMER_KEY'] = 'test_contextspace_key'
    os.environ['TWITTER_CONTEXTSPACE_CONSUMER_SECRET'] = 'test_contextspace_secret'
    os.environ['TWITTER_CONTEXTSPACE_ACCESS_TOKEN'] = 'test_contextspace_token'
    os.environ['TWITTER_CONTEXTSPACE_ACCESS_TOKEN_SECRET'] = 'test_contextspace_token_secret'
    os.environ['TWITTER_CONTEXTSPACE_BEARER_TOKEN'] = 'test_contextspace_bearer'
    
    # OSS Discoveries账号
    os.environ['TWITTER_OSSDISCOVERIES_CONSUMER_KEY'] = 'test_ossdiscoveries_key'
    os.environ['TWITTER_OSSDISCOVERIES_CONSUMER_SECRET'] = 'test_ossdiscoveries_secret'
    os.environ['TWITTER_OSSDISCOVERIES_ACCESS_TOKEN'] = 'test_ossdiscoveries_token'
    os.environ['TWITTER_OSSDISCOVERIES_ACCESS_TOKEN_SECRET'] = 'test_ossdiscoveries_token_secret'
    os.environ['TWITTER_OSSDISCOVERIES_BEARER_TOKEN'] = 'test_ossdiscoveries_bearer'
    
    # AI Flow Watch账号
    os.environ['TWITTER_AIFLOWWATCH_CONSUMER_KEY'] = 'test_aiflowwatch_key'
    os.environ['TWITTER_AIFLOWWATCH_CONSUMER_SECRET'] = 'test_aiflowwatch_secret'
    os.environ['TWITTER_AIFLOWWATCH_ACCESS_TOKEN'] = 'test_aiflowwatch_token'
    os.environ['TWITTER_AIFLOWWATCH_ACCESS_TOKEN_SECRET'] = 'test_aiflowwatch_token_secret'
    os.environ['TWITTER_AIFLOWWATCH_BEARER_TOKEN'] = 'test_aiflowwatch_bearer'
    
    # Open Source Reader账号
    os.environ['TWITTER_OPENSOURCEREADER_CONSUMER_KEY'] = 'test_opensourcereader_key'
    os.environ['TWITTER_OPENSOURCEREADER_CONSUMER_SECRET'] = 'test_opensourcereader_secret'
    os.environ['TWITTER_OPENSOURCEREADER_ACCESS_TOKEN'] = 'test_opensourcereader_token'
    os.environ['TWITTER_OPENSOURCEREADER_ACCESS_TOKEN_SECRET'] = 'test_opensourcereader_token_secret'
    os.environ['TWITTER_OPENSOURCEREADER_BEARER_TOKEN'] = 'test_opensourcereader_bearer'

def test_account_mapping():
    """测试账号映射"""
    print("🔍 测试账号映射逻辑")
    print("=" * 60)
    
    # 设置测试环境
    setup_test_env()
    
    # 导入配置类
    from twitter_accounts_config import TwitterAccountsConfig
    
    # 初始化配置
    config = TwitterAccountsConfig()
    
    print(f"\n📊 加载的账号配置 ({len(config.accounts)} 个):")
    for account_name in config.accounts:
        print(f"  ✅ {account_name}")
    
    # 测试四个目标账号的映射
    print("\n🧪 测试账号映射:")
    test_cases = [
        "ContextSpace",
        "OSS Discoveries", 
        "Ai flow watch",
        "Open source reader"
    ]
    
    for test_case in test_cases:
        print(f"\n🎯 测试账号: '{test_case}'")
        
        # 显示标准化过程
        normalized = test_case.lower().strip()
        print(f"   标准化后: '{normalized}'")
        
        # 检查直接匹配
        if normalized in config.accounts:
            print(f"   ✅ 直接匹配: '{normalized}' 在accounts中")
        else:
            print(f"   ❌ 直接匹配: '{normalized}' 不在accounts中")
        
        # 检查映射匹配
        account_mapping = {
            'contextspace': 'contextspace',
            'context space': 'contextspace',
            'twitter': 'contextspace',
            'oss discoveries': 'ossdiscoveries',
            'ossdiscoveries': 'ossdiscoveries',
            'ai flow watch': 'aiflowwatch',
            'aiflowwatch': 'aiflowwatch',
            'open source reader': 'opensourcereader',
            'opensource reader': 'opensourcereader',
            'opensourcereader': 'opensourcereader',
        }
        
        if normalized in account_mapping:
            mapped_name = account_mapping[normalized]
            print(f"   📋 映射到: '{mapped_name}'")
            
            if mapped_name in config.accounts:
                print(f"   ✅ 映射成功: '{mapped_name}' 在accounts中")
            else:
                print(f"   ❌ 映射失败: '{mapped_name}' 不在accounts中")
        else:
            print(f"   ❌ 无映射: '{normalized}' 不在映射表中")
        
        # 实际调用get_account_config测试
        result = config.get_account_config(test_case)
        if result:
            account_name = result.get('account_name', 'unknown')
            print(f"   🎉 最终结果: 成功找到配置 (账号: {account_name})")
        else:
            print(f"   💥 最终结果: 配置未找到")
    
    print("\n" + "=" * 60)
    print("🔧 推荐修复方案:")
    print("1. 检查环境变量命名是否严格匹配")
    print("2. 确认映射表中包含所有可能的输入变体")
    print("3. 添加调试日志输出中间步骤")

if __name__ == "__main__":
    test_account_mapping() 