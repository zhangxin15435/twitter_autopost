#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书文章自动发布到Twitter的主程序
从飞书多维表格获取文章内容，自动发布到Twitter
"""

import os
import sys
import time
import logging
from datetime import datetime
from typing import Optional, Dict
from dotenv import load_dotenv

# 导入自定义模块
from connect_feishu import FeishuAPI
from connect_twitter import TwitterAPI

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('twitter_auto_bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TwitterAutoBot:
    """Twitter自动发布机器人"""
    
    def __init__(self):
        """初始化机器人"""
        self.feishu = None
        self.twitter = None
        self.debug = os.getenv('DEBUG', 'False').lower() == 'true'
        
        # 初始化API连接
        self._init_apis()
    
    def _init_apis(self):
        """初始化API连接"""
        try:
            # 初始化飞书API
            self.feishu = FeishuAPI()
            logger.info("飞书API初始化成功")
            
            # 初始化Twitter API
            self.twitter = TwitterAPI()
            logger.info("Twitter API初始化成功")
            
            # 测试连接
            if not self.test_connections():
                raise Exception("API连接测试失败")
                
        except Exception as e:
            logger.error(f"初始化API时发生错误: {str(e)}")
            raise
    
    def test_connections(self) -> bool:
        """测试API连接"""
        try:
            # 测试飞书连接
            feishu_test = self.feishu.get_access_token()
            if not feishu_test:
                logger.error("飞书API连接失败")
                return False
            
            # 测试Twitter连接
            twitter_test = self.twitter.test_connection()
            if not twitter_test:
                logger.error("Twitter API连接失败")
                return False
            
            logger.info("所有API连接测试通过")
            return True
            
        except Exception as e:
            logger.error(f"测试API连接时发生错误: {str(e)}")
            return False
    
    def get_article_from_feishu(self) -> Optional[Dict]:
        """从飞书获取文章内容"""
        try:
            article = self.feishu.get_article_content()
            if article:
                logger.info(f"从飞书获取文章成功: {article.get('title', 'Unknown')}")
                return article
            else:
                logger.warning("没有可用的文章内容")
                return None
                
        except Exception as e:
            logger.error(f"从飞书获取文章时发生错误: {str(e)}")
            return None
    
    def publish_to_twitter(self, article_data: Dict) -> bool:
        """发布文章到Twitter"""
        try:
            # 格式化推文内容
            tweet_content = self.twitter.format_tweet_content(article_data)
            
            if self.debug:
                logger.info(f"调试模式 - 推文内容:\n{tweet_content}")
                logger.info(f"推文长度: {len(tweet_content)} 字符")
                return True
            
            # 发布推文
            tweet_result = self.twitter.create_tweet(tweet_content)
            
            if tweet_result:
                logger.info(f"推文发布成功: {tweet_result.get('url', 'Unknown')}")
                
                # 标记文章为已发布
                record_id = article_data.get('record_id')
                if record_id:
                    self.feishu.mark_as_published(record_id)
                    logger.info(f"文章 {record_id} 已标记为已发布")
                
                return True
            else:
                logger.error("推文发布失败")
                return False
                
        except Exception as e:
            logger.error(f"发布推文时发生错误: {str(e)}")
            return False
    
    def run_once(self) -> bool:
        """执行一次发布任务"""
        try:
            logger.info("开始执行发布任务")
            
            # 获取文章内容
            article = self.get_article_from_feishu()
            if not article:
                logger.warning("没有可发布的文章")
                return False
            
            # 发布到Twitter
            success = self.publish_to_twitter(article)
            
            if success:
                logger.info("发布任务完成")
                return True
            else:
                logger.error("发布任务失败")
                return False
                
        except Exception as e:
            logger.error(f"执行发布任务时发生错误: {str(e)}")
            return False
    
    def run_scheduled(self):
        """运行定时任务（由外部调度器调用）"""
        try:
            logger.info("=" * 50)
            logger.info(f"定时任务开始 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            success = self.run_once()
            
            if success:
                logger.info("定时任务执行成功")
            else:
                logger.error("定时任务执行失败")
            
            logger.info("=" * 50)
            
        except Exception as e:
            logger.error(f"定时任务执行时发生错误: {str(e)}")
    
    def get_status(self) -> Dict:
        """获取机器人状态"""
        try:
            status = {
                'timestamp': datetime.now().isoformat(),
                'feishu_connected': False,
                'twitter_connected': False,
                'debug_mode': self.debug
            }
            
            # 检查飞书连接
            try:
                self.feishu.get_access_token()
                status['feishu_connected'] = True
            except:
                pass
            
            # 检查Twitter连接
            try:
                status['twitter_connected'] = self.twitter.test_connection()
            except:
                pass
            
            return status
            
        except Exception as e:
            logger.error(f"获取状态时发生错误: {str(e)}")
            return {}


def main():
    """主程序入口"""
    try:
        # 解析命令行参数
        if len(sys.argv) > 1:
            command = sys.argv[1].lower()
        else:
            command = 'run'
        
        # 创建机器人实例
        bot = TwitterAutoBot()
        
        if command == 'test':
            # 测试模式
            logger.info("运行测试模式")
            
            # 测试连接
            if bot.test_connections():
                print("✅ API连接测试通过")
            else:
                print("❌ API连接测试失败")
                return
            
            # 测试获取文章
            article = bot.get_article_from_feishu()
            if article:
                print(f"✅ 成功获取文章: {article.get('title', 'Unknown')}")
                
                # 测试格式化推文
                tweet_content = bot.twitter.format_tweet_content(article)
                print(f"✅ 推文内容预览:\n{tweet_content}")
                print(f"✅ 推文长度: {len(tweet_content)} 字符")
            else:
                print("❌ 无法获取文章")
        
        elif command == 'status':
            # 状态查看
            status = bot.get_status()
            print("机器人状态:")
            for key, value in status.items():
                print(f"  {key}: {value}")
        
        elif command == 'run':
            # 执行一次发布
            logger.info("执行单次发布任务")
            success = bot.run_once()
            if success:
                print("✅ 发布任务完成")
            else:
                print("❌ 发布任务失败")
        
        elif command == 'schedule':
            # 定时任务模式（由GitHub Actions调用）
            bot.run_scheduled()
        
        else:
            print(f"未知命令: {command}")
            print("可用命令: test, status, run, schedule")
    
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.error(f"程序运行时发生错误: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 