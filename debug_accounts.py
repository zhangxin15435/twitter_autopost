#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试脚本：检查Twitter账号配置状态
"""

import os
from twitter_accounts_config import TwitterAccountsConfig

def debug_accounts():
    """调试账号配置"""
    print("🔍 调试Twitter账号配置")
    print("=" * 50)
    
    # 检查所有TWITTER相关的环境变量
    print("\n📋 所有TWITTER环境变量:")
    twitter_vars = {}
    for key, value in os.environ.items():
        if key.startswith('TWITTER_'):
            # 隐藏敏感信息，只显示前8个字符
            safe_value = value[:8] + "..." if len(value) > 8 else value
            twitter_vars[key] = safe_value
            print(f"  {key} = {safe_value}")
    
    if not twitter_vars:
        print("  ❌ 没有找到TWITTER相关的环境变量")
        return
    
    # 检查账号名称推导
    print("\n🎯 从环境变量推导的账号名称:")
    account_names = set()
    for key in os.environ.keys():
        if key.startswith('TWITTER_') and key.endswith('_CONSUMER_KEY'):
            # 提取账号名称
            account_name = key[8:-13].lower()  # 去掉TWITTER_和_CONSUMER_KEY
            account_names.add(account_name)
            print(f"  {key} -> {account_name}")
    
    if not account_names:
        print("  ❌ 没有找到有效的账号配置")
        return
    
    # 初始化配置管理器
    print("\n⚙️ 加载账号配置:")
    config = TwitterAccountsConfig()
    
    # 显示已加载的账号
    print(f"\n📊 已加载的账号配置 ({len(config.accounts)}个):")
    for account_name, account_config in config.accounts.items():
        print(f"  ✅ {account_name}")
        if 'account_name' in account_config:
            print(f"     账号名: {account_config['account_name']}")
    
    # 测试四个目标账号的映射
    print("\n🧪 测试账号映射:")
    test_accounts = [
        "ContextSpace",
        "OSS Discoveries", 
        "Ai flow watch",
        "Open source reader"
    ]
    
    for test_account in test_accounts:
        account_config = config.get_account_config(test_account)
        if account_config:
            print(f"  ✅ '{test_account}' -> 找到配置")
        else:
            print(f"  ❌ '{test_account}' -> 配置未找到")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    debug_accounts() 