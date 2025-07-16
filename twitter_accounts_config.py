#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitter多账号配置管理模块
支持配置和管理多个Twitter账号
"""

import os
import json
import logging
from typing import Dict, Optional, List
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TwitterAccountsConfig:
    """Twitter多账号配置管理类"""
    
    def __init__(self, config_file: str = "twitter_accounts.json"):
        """初始化账号配置管理"""
        self.config_file = config_file
        self.accounts = {}
        self.load_accounts()
    
    def load_accounts(self):
        """加载账号配置"""
        try:
            # 优先从环境变量读取配置
            self.load_from_env()
            
            # 如果配置文件存在，也尝试加载
            if os.path.exists(self.config_file):
                self.load_from_file()
            
            logger.info(f"已加载 {len(self.accounts)} 个Twitter账号配置")
            
        except Exception as e:
            logger.error(f"加载账号配置失败: {str(e)}")
    
    def load_from_env(self):
        """从环境变量加载账号配置"""
        try:
            # 默认账号（向后兼容）
            default_account = self.get_account_from_env()
            if default_account:
                self.accounts['default'] = default_account
                logger.info("加载默认账号配置成功")
            
            # 多账号配置（格式：TWITTER_ACCOUNT_NAME_CONSUMER_KEY）
            account_names = set()
            for key in os.environ.keys():
                if key.startswith('TWITTER_') and key.endswith('_CONSUMER_KEY'):
                    # 提取账号名称
                    account_name = key[8:-13].lower()  # 去掉TWITTER_和_CONSUMER_KEY
                    account_names.add(account_name)
            
            # 为每个账号加载配置
            for account_name in account_names:
                account_config = self.get_account_from_env(account_name)
                if account_config:
                    self.accounts[account_name] = account_config
                    logger.info(f"加载账号 '{account_name}' 配置成功")
            
        except Exception as e:
            logger.error(f"从环境变量加载账号配置失败: {str(e)}")
    
    def get_account_from_env(self, account_name: str = None) -> Optional[Dict]:
        """从环境变量获取单个账号配置"""
        try:
            if account_name:
                # 多账号配置
                prefix = f"TWITTER_{account_name.upper()}_"
                api_key = os.getenv(f"{prefix}CONSUMER_KEY")
                api_secret = os.getenv(f"{prefix}CONSUMER_SECRET")
                access_token = os.getenv(f"{prefix}ACCESS_TOKEN")
                access_token_secret = os.getenv(f"{prefix}ACCESS_TOKEN_SECRET")
                bearer_token = os.getenv(f"{prefix}BEARER_TOKEN")
            else:
                # 默认账号配置
                api_key = os.getenv('TWITTER_CONSUMER_KEY')
                api_secret = os.getenv('TWITTER_CONSUMER_SECRET')
                access_token = os.getenv('TWITTER_ACCESS_TOKEN')
                access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
                bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
            
            if not all([api_key, api_secret, access_token, access_token_secret]):
                return None
            
            return {
                'api_key': api_key,
                'api_secret': api_secret,
                'access_token': access_token,
                'access_token_secret': access_token_secret,
                'bearer_token': bearer_token,
                'account_name': account_name or 'default'
            }
            
        except Exception as e:
            logger.error(f"获取账号配置失败: {str(e)}")
            return None
    
    def load_from_file(self):
        """从文件加载账号配置"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                file_accounts = json.load(f)
            
            # 合并文件配置（环境变量优先）
            for account_name, config in file_accounts.items():
                if account_name not in self.accounts:
                    self.accounts[account_name] = config
                    logger.info(f"从文件加载账号 '{account_name}' 配置")
            
        except Exception as e:
            logger.error(f"从文件加载账号配置失败: {str(e)}")
    
    def save_to_file(self):
        """保存配置到文件"""
        try:
            # 只保存非敏感信息
            save_data = {}
            for account_name, config in self.accounts.items():
                save_data[account_name] = {
                    'account_name': config.get('account_name', ''),
                    'display_name': config.get('display_name', ''),
                    'description': config.get('description', ''),
                    'enabled': config.get('enabled', True)
                }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"账号配置已保存到 {self.config_file}")
            
        except Exception as e:
            logger.error(f"保存账号配置失败: {str(e)}")
    
    def get_account_config(self, account_name: str) -> Optional[Dict]:
        """获取指定账号的配置"""
        # 账号名称映射 - 更新为用户需要的四个账号
        account_mapping = {
            # 主账号 - ContextSpace
            'contextspace': 'contextspace',
            'context space': 'contextspace',
            'twitter': 'contextspace',  # 默认映射到ContextSpace主账号
            
            # OSS Discoveries
            'oss discoveries': 'ossdiscoveries',
            'ossdiscoveries': 'ossdiscoveries',
            
            # AI Flow Watch
            'ai flow watch': 'aiflowwatch',
            'aiflowwatch': 'aiflowwatch',
            
            # Open Source Reader
            'open source reader': 'opensourcereader',
            'opensource reader': 'opensourcereader',
            'opensourcereader': 'opensourcereader',
        }
        
        # 标准化账号名称
        normalized_name = account_name.lower().strip()
        
        # 尝试直接匹配
        if normalized_name in self.accounts:
            return self.accounts[normalized_name]
        
        # 尝试映射匹配
        if normalized_name in account_mapping:
            mapped_name = account_mapping[normalized_name]
            if mapped_name in self.accounts:
                return self.accounts[mapped_name]
        
        # 尝试默认账号（ContextSpace主账号）
        if 'contextspace' in self.accounts:
            logger.warning(f"账号 '{account_name}' 配置未找到，使用ContextSpace主账号")
            return self.accounts['contextspace']
        
        # 向后兼容：尝试default账号
        if 'default' in self.accounts:
            logger.warning(f"账号 '{account_name}' 配置未找到，使用默认账号")
            return self.accounts['default']
        
        logger.error(f"账号 '{account_name}' 配置未找到")
        return None
    
    def get_all_accounts(self) -> List[str]:
        """获取所有已配置的账号名称"""
        return list(self.accounts.keys())
    
    def add_account(self, account_name: str, config: Dict):
        """添加账号配置"""
        self.accounts[account_name] = config
        logger.info(f"添加账号 '{account_name}' 配置成功")
    
    def remove_account(self, account_name: str):
        """移除账号配置"""
        if account_name in self.accounts:
            del self.accounts[account_name]
            logger.info(f"移除账号 '{account_name}' 配置成功")
    
    def validate_account(self, account_name: str) -> bool:
        """验证账号配置是否完整"""
        config = self.get_account_config(account_name)
        if not config:
            return False
        
        required_fields = ['api_key', 'api_secret', 'access_token', 'access_token_secret']
        return all(config.get(field) for field in required_fields)
    
    def get_account_display_info(self) -> Dict:
        """获取账号显示信息"""
        info = {}
        for account_name, config in self.accounts.items():
            info[account_name] = {
                'name': config.get('account_name', account_name),
                'display_name': config.get('display_name', account_name),
                'enabled': config.get('enabled', True),
                'configured': self.validate_account(account_name)
            }
        return info

def setup_account_mapping():
    """设置账号映射示例"""
    print("🔧 Twitter多账号配置设置")
    print("=" * 50)
    
    # 创建配置管理器
    config_manager = TwitterAccountsConfig()
    
    print("📋 当前配置的账号:")
    accounts_info = config_manager.get_account_display_info()
    
    if not accounts_info:
        print("   未找到任何账号配置")
        print("\n💡 四个账号配置方法:")
        print("   📱 1. ContextSpace主账号:")
        print("      TWITTER_CONTEXTSPACE_CONSUMER_KEY=contextspace_key")
        print("      TWITTER_CONTEXTSPACE_CONSUMER_SECRET=contextspace_secret")
        print("      TWITTER_CONTEXTSPACE_ACCESS_TOKEN=contextspace_token")
        print("      TWITTER_CONTEXTSPACE_ACCESS_TOKEN_SECRET=contextspace_token_secret")
        print("      TWITTER_CONTEXTSPACE_BEARER_TOKEN=contextspace_bearer")
        print("")
        print("   📱 2. OSS Discoveries账号:")
        print("      TWITTER_OSSDISCOVERIES_CONSUMER_KEY=oss_key")
        print("      TWITTER_OSSDISCOVERIES_CONSUMER_SECRET=oss_secret")
        print("      TWITTER_OSSDISCOVERIES_ACCESS_TOKEN=oss_token")
        print("      TWITTER_OSSDISCOVERIES_ACCESS_TOKEN_SECRET=oss_token_secret")
        print("      TWITTER_OSSDISCOVERIES_BEARER_TOKEN=oss_bearer")
        print("")
        print("   📱 3. AI Flow Watch账号:")
        print("      TWITTER_AIFLOWWATCH_CONSUMER_KEY=ai_key")
        print("      TWITTER_AIFLOWWATCH_CONSUMER_SECRET=ai_secret")
        print("      TWITTER_AIFLOWWATCH_ACCESS_TOKEN=ai_token")
        print("      TWITTER_AIFLOWWATCH_ACCESS_TOKEN_SECRET=ai_token_secret")
        print("      TWITTER_AIFLOWWATCH_BEARER_TOKEN=ai_bearer")
        print("")
        print("   📱 4. Open Source Reader账号:")
        print("      TWITTER_OPENSOURCEREADER_CONSUMER_KEY=reader_key")
        print("      TWITTER_OPENSOURCEREADER_CONSUMER_SECRET=reader_secret")
        print("      TWITTER_OPENSOURCEREADER_ACCESS_TOKEN=reader_token")
        print("      TWITTER_OPENSOURCEREADER_ACCESS_TOKEN_SECRET=reader_token_secret")
        print("      TWITTER_OPENSOURCEREADER_BEARER_TOKEN=reader_bearer")
        return
    
    for account_name, info in accounts_info.items():
        status = "✅ 已配置" if info['configured'] else "❌ 配置不完整"
        print(f"   {account_name}: {status}")
    
    print("\n🔄 账号映射规则:")
    print("   CSV表格中的'发布账号' → 实际Twitter账号")
    print("   'ContextSpace' 或 'twitter' → @ContextSpace主账号")
    print("   'OSS Discoveries' → @OSSDiscoveries")
    print("   'Ai flow watch' → @AIFlowWatch")
    print("   'Open source reader' → @OpenSourceReader")
    
    # 测试账号配置
    print("\n🧪 测试四个账号配置:")
    test_accounts = ['ContextSpace', 'OSS Discoveries', 'Ai flow watch', 'Open source reader']
    
    for test_account in test_accounts:
        config = config_manager.get_account_config(test_account)
        if config:
            print(f"   '{test_account}' → ✅ 配置找到")
        else:
            print(f"   '{test_account}' → ❌ 配置未找到")

if __name__ == "__main__":
    setup_account_mapping() 