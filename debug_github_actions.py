#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Actions调试脚本
用于诊断账号配置问题
"""

import os
import sys

def debug_github_actions():
    """在GitHub Actions环境中调试账号配置"""
    print("🔍 GitHub Actions环境调试")
    print("=" * 60)
    
    # 检查所有Twitter相关环境变量
    print("\n📋 扫描所有TWITTER环境变量:")
    twitter_vars = []
    for key in sorted(os.environ.keys()):
        if key.startswith('TWITTER_'):
            # 隐藏敏感信息，只显示前8个字符
            value = os.environ[key]
            safe_value = value[:8] + "..." if len(value) > 8 else value
            twitter_vars.append((key, safe_value))
    
    if twitter_vars:
        for key, safe_value in twitter_vars:
            print(f"  ✅ {key} = {safe_value}")
    else:
        print("  ❌ 没有找到TWITTER相关的环境变量")
        return
    
    # 检查账号推导
    print("\n🎯 从环境变量推导账号名称:")
    accounts_found = set()
    for key, _ in twitter_vars:
        if key.endswith('_CONSUMER_KEY'):
            account_name = key[8:-13].lower()
            accounts_found.add(account_name)
            print(f"  📍 {key} -> {account_name}")
    
    print(f"\n📊 推导出的账号列表: {list(accounts_found)}")
    
    # 测试TwitterAccountsConfig
    print("\n⚙️ 测试TwitterAccountsConfig:")
    try:
        from twitter_accounts_config import TwitterAccountsConfig
        config = TwitterAccountsConfig()
        
        print(f"📈 加载的账号配置: {list(config.accounts.keys())}")
        
        # 测试特定账号查找
        test_account = "OSS Discoveries"
        print(f"\n🧪 测试查找账号: '{test_account}'")
        result = config.get_account_config(test_account)
        
        if result:
            print(f"  ✅ 找到配置: {result.get('account_name', 'unknown')}")
        else:
            print(f"  ❌ 配置未找到")
            
    except Exception as e:
        print(f"  💥 错误: {str(e)}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    debug_github_actions() 