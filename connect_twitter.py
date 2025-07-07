#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitter API连接模块
用于发布推文和处理Twitter相关操作
"""

import os
import tweepy
import logging
from typing import Dict, Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TwitterAPI:
    """Twitter API连接类"""
    
    def __init__(self):
        """初始化Twitter API配置"""
        self.api_key = os.getenv('TWITTER_CONSUMER_KEY')
        self.api_secret = os.getenv('TWITTER_CONSUMER_SECRET')
        self.access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        self.bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        
        # 验证配置
        if not all([self.api_key, self.api_secret, self.access_token, self.access_token_secret]):
            raise ValueError("请检查Twitter API配置是否完整")
        
        # 初始化API客户端
        self.client = None
        self.api = None
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
            
            logger.info("Twitter API客户端初始化成功")
            
        except Exception as e:
            logger.error(f"初始化Twitter API客户端失败: {str(e)}")
            raise
    
    def test_connection(self) -> bool:
        """测试Twitter API连接"""
        try:
            # 测试API v2连接
            user = self.client.get_me()
            if user.data:
                logger.info(f"API v2连接成功, 用户: {user.data.username}")
                return True
            else:
                logger.error("API v2连接失败")
                return False
                
        except Exception as e:
            logger.error(f"测试Twitter API连接失败: {str(e)}")
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
                logger.info(f"推文发布成功，ID: {tweet_id}")
                return {
                    'id': tweet_id,
                    'text': content,
                    'url': f"https://twitter.com/user/status/{tweet_id}"
                }
            else:
                logger.error("推文发布失败")
                return None
                
        except Exception as e:
            logger.error(f"发布推文时发生错误: {str(e)}")
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
            logger.info(f"媒体上传成功，ID: {media.media_id}")
            return media.media_id
            
        except Exception as e:
            logger.error(f"上传媒体时发生错误: {str(e)}")
            return None
    
    def format_tweet_content(self, article_data: Dict) -> str:
        """
        格式化推文内容
        
        Args:
            article_data: 文章数据字典
            
        Returns:
            格式化后的推文内容
        """
        try:
            title = article_data.get('title', '')
            content = article_data.get('content', '')
            author = article_data.get('author', '')
            source = article_data.get('source', '')
            
            # 构建推文内容
            tweet_parts = []
            
            # 添加标题
            if title:
                tweet_parts.append(f"📝 {title}")
            
            # 添加内容（限制长度）
            if content:
                # 为其他信息预留空间
                remaining_length = 280 - len('\n'.join(tweet_parts)) - 50
                if len(content) > remaining_length:
                    content = content[:remaining_length-3] + "..."
                tweet_parts.append(f"\n{content}")
            
            # 添加作者和来源信息
            if author or source:
                info_parts = []
                if author:
                    info_parts.append(f"👤 {author}")
                if source:
                    info_parts.append(f"📚 {source}")
                
                if info_parts:
                    tweet_parts.append(f"\n{' | '.join(info_parts)}")
            
            # 添加标签
            tweet_parts.append("\n\n#文章分享 #内容创作")
            
            tweet_content = ''.join(tweet_parts)
            
            # 确保不超过280字符
            if len(tweet_content) > 280:
                # 重新计算，优先保留标题和作者信息
                base_info = f"📝 {title}\n"
                if author:
                    base_info += f"👤 {author}\n"
                base_info += "\n#文章分享 #内容创作"
                
                remaining_length = 280 - len(base_info) - 2  # 留2个字符缓冲
                if len(content) > remaining_length:
                    content = content[:remaining_length-3] + "..."
                
                tweet_content = f"📝 {title}\n{content}"
                if author:
                    tweet_content += f"\n👤 {author}"
                tweet_content += "\n\n#文章分享 #内容创作"
            
            return tweet_content
            
        except Exception as e:
            logger.error(f"格式化推文内容时发生错误: {str(e)}")
            # 返回简化版本
            return f"{article_data.get('title', 'Unknown')}\n{article_data.get('content', '')[:200]}..."
    
    def get_rate_limit_status(self) -> Dict:
        """获取API速率限制状态"""
        try:
            limits = self.api.get_rate_limit_status()
            return limits
        except Exception as e:
            logger.error(f"获取速率限制状态时发生错误: {str(e)}")
            return {}


def test_twitter_connection():
    """测试Twitter API连接"""
    try:
        twitter = TwitterAPI()
        
        # 测试连接
        if twitter.test_connection():
            print("Twitter API连接成功")
            
            # 测试格式化内容
            sample_article = {
                'title': '测试文章标题',
                'content': '这是一篇测试文章的内容，用于验证Twitter API的功能是否正常工作。',
                'author': '测试作者',
                'source': '测试来源'
            }
            
            formatted_content = twitter.format_tweet_content(sample_article)
            print(f"格式化后的推文内容:\n{formatted_content}")
            print(f"推文长度: {len(formatted_content)} 字符")
            
            return True
        else:
            print("Twitter API连接失败")
            return False
            
    except Exception as e:
        print(f"测试失败: {str(e)}")
        return False


if __name__ == "__main__":
    test_twitter_connection() 