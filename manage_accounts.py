#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitter账号管理工具
用于启用/禁用账号、查看账号状态等
"""

import sys
import argparse
from typing import Dict
from twitter_accounts_config import TwitterAccountsConfig

def show_accounts_status(config_manager: TwitterAccountsConfig):
    """显示所有账号状态"""
    print("=" * 60)
    print("🐦 Twitter账号状态管理")
    print("=" * 60)
    
    accounts_info = config_manager.get_account_display_info()
    
    if not accounts_info:
        print("❌ 未找到任何账号配置")
        return
    
    print(f"📋 共找到 {len(accounts_info)} 个账号:")
    print("")
    
    for account_name, info in accounts_info.items():
        # 状态图标
        enabled_icon = "🟢" if info['enabled'] else "🔴"
        config_icon = "✅" if info['configured'] else "❌"
        
        print(f"  {enabled_icon} {account_name}")
        print(f"     状态: {'启用' if info['enabled'] else '禁用'}")
        print(f"     配置: {'完整' if info['configured'] else '不完整'}")
        print(f"     显示名: {info.get('display_name', 'N/A')}")
        print("")
    
    print("说明:")
    print("  🟢 = 账号已启用")
    print("  🔴 = 账号已禁用")
    print("  ✅ = 配置完整")
    print("  ❌ = 配置不完整")

def enable_account(config_manager: TwitterAccountsConfig, account_name: str):
    """启用账号"""
    if config_manager.set_account_enabled(account_name, True):
        print(f"✅ 账号 '{account_name}' 已启用")
        return True
    else:
        print(f"❌ 启用账号 '{account_name}' 失败")
        return False

def disable_account(config_manager: TwitterAccountsConfig, account_name: str):
    """禁用账号"""
    if config_manager.set_account_enabled(account_name, False):
        print(f"🔴 账号 '{account_name}' 已禁用")
        return True
    else:
        print(f"❌ 禁用账号 '{account_name}' 失败")
        return False

def disable_contextspace_account():
    """禁用contextspace账号"""
    print("🔄 正在禁用ContextSpace账号...")
    config_manager = TwitterAccountsConfig()
    
    # 显示当前状态
    print("\n📊 当前账号状态:")
    show_accounts_status(config_manager)
    
    # 禁用contextspace账号
    print("\n🔴 正在禁用ContextSpace账号...")
    success = disable_account(config_manager, 'contextspace')
    
    if success:
        print("\n✅ ContextSpace账号已成功禁用！")
        print("\n📊 更新后的账号状态:")
        show_accounts_status(config_manager)
        print("\n💡 说明:")
        print("   - ContextSpace账号已暂时禁用，不会自动发布内容")
        print("   - 其他账号（OSS Discoveries、AI Flow Watch、Open Source Reader）仍可正常发布")
        print("   - 如需重新启用，请运行: python manage_accounts.py --enable contextspace")
    else:
        print("\n❌ 禁用ContextSpace账号失败！")
        print("请检查账号配置是否正确。")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Twitter账号管理工具')
    parser.add_argument('--status', action='store_true', help='显示所有账号状态')
    parser.add_argument('--enable', type=str, help='启用指定账号')
    parser.add_argument('--disable', type=str, help='禁用指定账号')
    parser.add_argument('--disable-contextspace', action='store_true', help='禁用ContextSpace账号')
    
    args = parser.parse_args()
    
    try:
        config_manager = TwitterAccountsConfig()
        
        if args.disable_contextspace:
            # 禁用contextspace账号
            disable_contextspace_account()
            
        elif args.status:
            # 显示账号状态
            show_accounts_status(config_manager)
            
        elif args.enable:
            # 启用账号
            account_name = args.enable
            print(f"🟢 正在启用账号 '{account_name}'...")
            success = enable_account(config_manager, account_name)
            if success:
                print("\n📊 更新后的账号状态:")
                show_accounts_status(config_manager)
            
        elif args.disable:
            # 禁用账号
            account_name = args.disable
            print(f"🔴 正在禁用账号 '{account_name}'...")
            success = disable_account(config_manager, account_name)
            if success:
                print("\n📊 更新后的账号状态:")
                show_accounts_status(config_manager)
            
        else:
            # 没有参数，显示帮助信息
            print("🐦 Twitter账号管理工具")
            print("=" * 40)
            print("用法:")
            print("  python manage_accounts.py --status                    # 查看所有账号状态")
            print("  python manage_accounts.py --disable-contextspace      # 禁用ContextSpace账号")
            print("  python manage_accounts.py --enable contextspace       # 启用ContextSpace账号")
            print("  python manage_accounts.py --disable ossdiscoveries    # 禁用OSS Discoveries账号")
            print("  python manage_accounts.py --enable aiflowwatch        # 启用AI Flow Watch账号")
            print("")
            print("支持的账号名称:")
            print("  - contextspace      (ContextSpace主账号)")
            print("  - ossdiscoveries    (OSS Discoveries)")
            print("  - aiflowwatch       (AI Flow Watch)")
            print("  - opensourcereader  (Open Source Reader)")
            
    except Exception as e:
        print(f"❌ 执行时发生错误: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 