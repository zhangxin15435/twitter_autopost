#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitter多账号API连接模块
支持根据账号配置连接不同的Twitter账号
"""

import os
import tweepy
import logging
from typing import Dict, Optional, List
from dotenv import load_dotenv
from twitter_accounts_config import TwitterAccountsConfig

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MultiTwitterAPI:
    """多账号Twitter API连接类"""
    
    def __init__(self, account_config: Dict = None):
        """初始化Twitter API配置"""
        if account_config:
            self.api_key = account_config.get('api_key')
            self.api_secret = account_config.get('api_secret')
            self.access_token = account_config.get('access_token')
            self.access_token_secret = account_config.get('access_token_secret')
            self.bearer_token = account_config.get('bearer_token')
            self.account_name = account_config.get('account_name', 'unknown')
        else:
            # 向后兼容，使用环境变量
            self.api_key = os.getenv('TWITTER_CONSUMER_KEY')
            self.api_secret = os.getenv('TWITTER_CONSUMER_SECRET')
            self.access_token = os.getenv('TWITTER_ACCESS_TOKEN')
            self.access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
            self.bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
            self.account_name = 'default'
        
        # 验证配置
        if not all([self.api_key, self.api_secret, self.access_token, self.access_token_secret]):
            raise ValueError(f"Twitter API配置不完整 (账号: {self.account_name})")
        
        # 初始化API客户端
        self.client = None
        self.api = None
        self.username = None
        self._init_clients()
    
    def _init_clients(self):
        """初始化Twitter API客户端"""
        try:
            # 初始化v2客户端（用于新功能）
            self.client = tweepy.Client(
                bearer_token=self.bearer_token,
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret,
                wait_on_rate_limit=True
            )
            
            # 初始化v1.1客户端（用于兼容性）
            auth = tweepy.OAuth1UserHandler(
                self.api_key,
                self.api_secret,
                self.access_token,
                self.access_token_secret
            )
            self.api = tweepy.API(auth, wait_on_rate_limit=True)
            
            logger.info(f"Twitter API客户端初始化成功 (账号: {self.account_name})")
            
        except Exception as e:
            logger.error(f"初始化Twitter API客户端失败 (账号: {self.account_name}): {str(e)}")
            raise
    
    def test_connection(self) -> bool:
        """测试Twitter API连接"""
        try:
            # 测试API v2连接
            user = self.client.get_me()
            if user.data:
                self.username = user.data.username
                logger.info(f"API v2连接成功 (账号: {self.account_name}, 用户: @{self.username})")
                return True
            else:
                logger.error(f"API v2连接失败 (账号: {self.account_name})")
                return False
                
        except Exception as e:
            logger.error(f"测试Twitter API连接失败 (账号: {self.account_name}): {str(e)}")
            return False
    
    def create_tweet(self, content: str, media_ids: Optional[list] = None) -> Optional[Dict]:
        """
        发布推文
        
        Args:
            content: 推文内容
            media_ids: 媒体ID列表（可选）
            
        Returns:
            推文信息字典或None
        """
        try:
            if len(content) > 280:
                logger.warning(f"推文内容过长 ({len(content)} 字符)，将被截断")
                content = content[:277] + "..."
            
            # 发布推文
            response = self.client.create_tweet(
                text=content,
                media_ids=media_ids
            )
            
            if response.data:
                tweet_id = response.data['id']
                logger.info(f"推文发布成功 (账号: @{self.username}, ID: {tweet_id})")
                return {
                    'id': tweet_id,
                    'text': content,
                    'url': f"https://twitter.com/{self.username}/status/{tweet_id}",
                    'account': self.account_name,
                    'username': self.username
                }
            else:
                logger.error(f"推文发布失败 (账号: {self.account_name})")
                return None
                
        except Exception as e:
            logger.error(f"发布推文时发生错误 (账号: {self.account_name}): {str(e)}")
            return None
    
    def upload_media(self, media_path: str) -> Optional[str]:
        """
        上传媒体文件
        
        Args:
            media_path: 媒体文件路径
            
        Returns:
            媒体ID或None
        """
        try:
            if not os.path.exists(media_path):
                logger.error(f"媒体文件不存在: {media_path}")
                return None
            
            # 使用v1.1 API上传媒体
            media = self.api.media_upload(media_path)
            logger.info(f"媒体上传成功 (账号: {self.account_name}, ID: {media.media_id})")
            return media.media_id
            
        except Exception as e:
            logger.error(f"上传媒体时发生错误 (账号: {self.account_name}): {str(e)}")
            return None
    
    def get_rate_limit_status(self) -> Dict:
        """获取API速率限制状态"""
        try:
            limits = self.api.get_rate_limit_status()
            return limits
        except Exception as e:
            logger.error(f"获取速率限制状态时发生错误 (账号: {self.account_name}): {str(e)}")
            return {}

class TwitterAccountManager:
    """Twitter账号管理器"""
    
    def __init__(self):
        """初始化账号管理器"""
        self.accounts_config = TwitterAccountsConfig()
        self.active_apis = {}  # 缓存已连接的API实例
    
    def get_api_for_account(self, account_name: str) -> Optional[MultiTwitterAPI]:
        """获取指定账号的API实例"""
        try:
            # 如果已经有缓存的API实例，直接返回
            if account_name in self.active_apis:
                return self.active_apis[account_name]
            
            # 获取账号配置
            config = self.accounts_config.get_account_config(account_name)
            if not config:
                logger.error(f"账号 '{account_name}' 配置未找到")
                return None
            
            # 创建API实例
            api = MultiTwitterAPI(config)
            
            # 测试连接
            if api.test_connection():
                # 缓存成功连接的API实例
                self.active_apis[account_name] = api
                logger.info(f"账号 '{account_name}' API连接成功")
                return api
            else:
                logger.error(f"账号 '{account_name}' API连接失败")
                return None
                
        except Exception as e:
            logger.error(f"获取账号 '{account_name}' API时发生错误: {str(e)}")
            return None
    
    def publish_tweet(self, account_name: str, content: str) -> Optional[Dict]:
        """发布推文到指定账号"""
        try:
            api = self.get_api_for_account(account_name)
            if not api:
                return None
            
            return api.create_tweet(content)
            
        except Exception as e:
            logger.error(f"发布推文到账号 '{account_name}' 时发生错误: {str(e)}")
            return None
    
    def get_available_accounts(self) -> List[str]:
        """获取所有可用的账号"""
        return self.accounts_config.get_all_accounts()
    
    def test_all_accounts(self) -> Dict:
        """测试所有账号的连接状态"""
        results = {}
        accounts = self.get_available_accounts()
        
        for account_name in accounts:
            try:
                api = self.get_api_for_account(account_name)
                if api:
                    results[account_name] = {
                        'status': 'success',
                        'username': api.username,
                        'account_name': api.account_name
                    }
                else:
                    results[account_name] = {
                        'status': 'failed',
                        'error': 'API连接失败'
                    }
            except Exception as e:
                results[account_name] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        return results

def test_multi_account_setup():
    """测试多账号设置"""
    print("🧪 测试Twitter多账号设置")
    print("=" * 50)
    
    try:
        # 创建账号管理器
        manager = TwitterAccountManager()
        
        # 测试所有账号
        test_results = manager.test_all_accounts()
        
        print("📋 账号测试结果:")
        for account_name, result in test_results.items():
            if result['status'] == 'success':
                print(f"   ✅ {account_name} (@{result['username']})")
            else:
                print(f"   ❌ {account_name} - {result.get('error', '未知错误')}")
        
        # 测试表格中的账号映射
        print("\n🔄 测试账号映射:")
        test_accounts = ['ai flow watch', 'OpenSource Radar', 'oss discoveries', 'twitter']
        
        for test_account in test_accounts:
            api = manager.get_api_for_account(test_account)
            if api:
                print(f"   '{test_account}' → ✅ @{api.username}")
            else:
                print(f"   '{test_account}' → ❌ 配置未找到")
        
        return len([r for r in test_results.values() if r['status'] == 'success']) > 0
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    test_multi_account_setup() 