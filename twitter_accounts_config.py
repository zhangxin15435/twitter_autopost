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
        # 账号启用/禁用状态（内存中存储，可持久化到文件）
        self.account_enabled_status = {}
        self.load_accounts()
        self.load_enabled_status()
    
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
    
    def load_enabled_status(self):
        """加载账号启用状态"""
        try:
            status_file = "twitter_accounts_status.json"
            if os.path.exists(status_file):
                with open(status_file, 'r', encoding='utf-8') as f:
                    self.account_enabled_status = json.load(f)
                logger.info(f"已加载账号启用状态配置")
            else:
                # 默认所有账号都启用
                for account_name in self.accounts.keys():
                    self.account_enabled_status[account_name] = True
                logger.info("使用默认账号启用状态（全部启用）")
        except Exception as e:
            logger.error(f"加载账号启用状态失败: {str(e)}")
            # 如果加载失败，默认所有账号都启用
            for account_name in self.accounts.keys():
                self.account_enabled_status[account_name] = True
    
    def save_enabled_status(self):
        """保存账号启用状态"""
        try:
            status_file = "twitter_accounts_status.json"
            with open(status_file, 'w', encoding='utf-8') as f:
                json.dump(self.account_enabled_status, f, indent=2, ensure_ascii=False)
            logger.info(f"账号启用状态已保存到 {status_file}")
        except Exception as e:
            logger.error(f"保存账号启用状态失败: {str(e)}")
    
    def set_account_enabled(self, account_name: str, enabled: bool):
        """设置账号启用/禁用状态"""
        # 获取实际账号名称（处理映射）
        actual_account = self._get_actual_account_name(account_name)
        
        if actual_account and actual_account in self.accounts:
            self.account_enabled_status[actual_account] = enabled
            self.save_enabled_status()
            status_text = "启用" if enabled else "禁用"
            logger.info(f"账号 '{actual_account}' 已{status_text}")
            return True
        else:
            logger.error(f"账号 '{account_name}' 不存在，无法设置状态")
            return False
    
    def is_account_enabled(self, account_name: str) -> bool:
        """检查账号是否启用"""
        # 获取实际账号名称（处理映射）
        actual_account = self._get_actual_account_name(account_name)
        
        if actual_account and actual_account in self.accounts:
            return self.account_enabled_status.get(actual_account, True)
        return False
    
    def _get_actual_account_name(self, account_name: str) -> Optional[str]:
        """获取实际的账号名称（处理映射）"""
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
        
        normalized_name = account_name.lower().strip()
        
        # 尝试直接匹配
        if normalized_name in self.accounts:
            return normalized_name
        
        # 尝试映射匹配
        if normalized_name in account_mapping:
            mapped_name = account_mapping[normalized_name]
            if mapped_name in self.accounts:
                return mapped_name
        
        return None
    
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
            logger.info("扫描环境变量中的Twitter账号配置...")
            for key in os.environ.keys():
                if key.startswith('TWITTER_') and key.endswith('_CONSUMER_KEY'):
                    # 提取账号名称
                    account_name = key[8:-13].lower()  # 去掉TWITTER_和_CONSUMER_KEY
                    account_names.add(account_name)
                    logger.info(f"发现账号环境变量: {key} -> {account_name}")
            
            logger.info(f"找到 {len(account_names)} 个账号: {list(account_names)}")
            
            # 为每个账号加载配置
            for account_name in account_names:
                logger.info(f"尝试加载账号 '{account_name}' 的配置...")
                account_config = self.get_account_from_env(account_name)
                if account_config:
                    self.accounts[account_name] = account_config
                    logger.info(f"✅ 加载账号 '{account_name}' 配置成功")
                else:
                    logger.warning(f"❌ 加载账号 '{account_name}' 配置失败")
            
        except Exception as e:
            logger.error(f"从环境变量加载账号配置失败: {str(e)}")
    
    def get_account_from_env(self, account_name: str = None) -> Optional[Dict]:
        """从环境变量获取单个账号配置"""
        try:
            if account_name:
                # 多账号配置
                prefix = f"TWITTER_{account_name.upper()}_"
                logger.info(f"查找环境变量前缀: {prefix}")
                api_key = os.getenv(f"{prefix}CONSUMER_KEY")
                api_secret = os.getenv(f"{prefix}CONSUMER_SECRET")
                access_token = os.getenv(f"{prefix}ACCESS_TOKEN")
                access_token_secret = os.getenv(f"{prefix}ACCESS_TOKEN_SECRET")
                bearer_token = os.getenv(f"{prefix}BEARER_TOKEN")
                
                # 调试输出
                logger.info(f"API密钥状态: key={'✅' if api_key else '❌'}, secret={'✅' if api_secret else '❌'}, token={'✅' if access_token else '❌'}, token_secret={'✅' if access_token_secret else '❌'}")
            else:
                # 默认账号配置
                api_key = os.getenv('TWITTER_CONSUMER_KEY')
                api_secret = os.getenv('TWITTER_CONSUMER_SECRET')
                access_token = os.getenv('TWITTER_ACCESS_TOKEN')
                access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
                bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
            
            if not all([api_key, api_secret, access_token, access_token_secret]):
                missing = []
                if not api_key: missing.append("CONSUMER_KEY")
                if not api_secret: missing.append("CONSUMER_SECRET") 
                if not access_token: missing.append("ACCESS_TOKEN")
                if not access_token_secret: missing.append("ACCESS_TOKEN_SECRET")
                logger.warning(f"账号 '{account_name or 'default'}' 配置不完整，缺少: {', '.join(missing)}")
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
        """获取指定账号的配置（只返回启用的账号）"""
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
        logger.info(f"查找账号配置: '{account_name}' -> 标准化: '{normalized_name}'")
        logger.info(f"当前可用账号: {list(self.accounts.keys())}")
        
        # 先检查目标账号
        target_account = None
        
        # 尝试直接匹配
        if normalized_name in self.accounts:
            target_account = normalized_name
            logger.info(f"直接匹配成功: '{normalized_name}'")
        # 尝试映射匹配
        elif normalized_name in account_mapping:
            mapped_name = account_mapping[normalized_name]
            logger.info(f"账号映射: '{normalized_name}' -> '{mapped_name}'")
            if mapped_name in self.accounts:
                target_account = mapped_name
                logger.info(f"映射匹配成功: '{mapped_name}'")
            else:
                logger.warning(f"映射失败: '{mapped_name}' 不在可用账号中")
        
        # 如果找到目标账号，检查是否启用
        if target_account:
            if self.is_account_enabled(target_account):
                logger.info(f"账号 '{target_account}' 已启用，返回配置")
                return self.accounts[target_account]
            else:
                logger.warning(f"账号 '{target_account}' 已禁用，跳过发布")
                return None
        
        # 如果没有找到账号，尝试默认账号（但要检查启用状态）
        logger.warning(f"无映射规则: '{normalized_name}' 不在映射表中")
        
        # 尝试默认账号（ContextSpace主账号）
        if 'contextspace' in self.accounts:
            if self.is_account_enabled('contextspace'):
                logger.warning(f"账号 '{account_name}' 配置未找到，使用ContextSpace主账号")
                return self.accounts['contextspace']
            else:
                logger.warning(f"ContextSpace主账号已禁用，无法使用")
        
        # 向后兼容：尝试default账号
        if 'default' in self.accounts:
            if self.is_account_enabled('default'):
                logger.warning(f"账号 '{account_name}' 配置未找到，使用默认账号")
                return self.accounts['default']
            else:
                logger.warning(f"默认账号已禁用，无法使用")
        
        logger.error(f"账号 '{account_name}' 配置未找到或所有相关账号已禁用")
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
                'enabled': self.is_account_enabled(account_name),  # 使用实际启用状态
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