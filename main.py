#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitter自动发布主程序
从CSV文件读取内容并自动发布到Twitter，支持多账号发布
"""

import os
import sys
import logging
from datetime import datetime
from typing import Optional, Dict

# 导入多账号发布模块
try:
    from main_multi_account import MultiAccountTwitterPublisher
except ImportError:
    print("❌ 无法导入多账号发布模块，请检查文件是否存在")
    sys.exit(1)

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
    """Twitter自动发布机器人 - 纯Twitter版本"""
    
    def __init__(self):
        """初始化机器人"""
        self.publisher = MultiAccountTwitterPublisher()
        self.debug = os.getenv('DEBUG', 'False').lower() == 'true'
        
        logger.info("Twitter自动发布机器人初始化完成（纯Twitter版本）")
    
    def test_connections(self) -> bool:
        """测试Twitter连接"""
        try:
            # 测试多账号配置
            results = self.publisher.test_all_accounts()
            
            success_count = sum(1 for result in results.values() if result.get('status') == 'success')
            total_count = len(results)
            
            logger.info(f"Twitter账号连接测试: {success_count}/{total_count} 个账号连接成功")
            
            if success_count > 0:
                logger.info("✅ 至少有一个Twitter账号可用")
                return True
            else:
                logger.error("❌ 没有可用的Twitter账号")
                return False
                
        except Exception as e:
            logger.error(f"测试Twitter连接时发生错误: {str(e)}")
            return False
    
    def get_next_article(self) -> Optional[Dict]:
        """获取下一篇待发布的文章"""
        try:
            article = self.publisher.get_next_article()
            if article:
                logger.info(f"获取文章成功: {article.get('title', 'Unknown')}")
                return article
            else:
                logger.warning("没有可用的文章内容")
                return None
                
        except Exception as e:
            logger.error(f"获取文章时发生错误: {str(e)}")
            return None
    
    def publish_to_twitter(self, article_data: Dict) -> bool:
        """发布文章到Twitter"""
        try:
            if self.debug:
                logger.info(f"调试模式 - 文章内容:")
                logger.info(f"  标题: {article_data.get('title', 'Unknown')}")
                logger.info(f"  发布账号: {article_data.get('publish_account', 'default')}")
                logger.info(f"  内容: {article_data.get('content', '')[:100]}...")
                return True
            
            # 发布推文
            success = self.publisher.publish_article(article_data)
            
            if success:
                logger.info("✅ 推文发布成功")
                return True
            else:
                logger.error("❌ 推文发布失败")
                return False
                
        except Exception as e:
            logger.error(f"发布推文时发生错误: {str(e)}")
            return False
    
    def run_once(self) -> bool:
        """执行一次发布任务"""
        try:
            logger.info("🚀 开始执行发布任务")
            
            # 获取文章内容
            article = self.get_next_article()
            if not article:
                logger.warning("没有可发布的文章")
                return False
            
            # 发布到Twitter
            success = self.publish_to_twitter(article)
            
            if success:
                logger.info("✅ 发布任务完成")
                return True
            else:
                logger.error("❌ 发布任务失败")
                return False
                
        except Exception as e:
            logger.error(f"执行发布任务时发生错误: {str(e)}")
            return False
    
    def run_scheduled(self):
        """运行定时任务（由外部调度器调用）"""
        try:
            logger.info("=" * 50)
            logger.info(f"定时任务开始 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # 使用多账号发布器执行任务
            success = self.publisher.run_once()
            
            if success:
                logger.info("✅ 定时任务执行成功")
            else:
                logger.error("❌ 定时任务执行失败")
            
            logger.info("=" * 50)
            
        except Exception as e:
            logger.error(f"定时任务执行时发生错误: {str(e)}")
    
    def get_status(self) -> Dict:
        """获取机器人状态"""
        try:
            # 获取统计信息
            stats = self.publisher.get_statistics()
            
            # 获取账号状态
            account_results = self.publisher.test_all_accounts()
            
            status = {
                'timestamp': datetime.now().isoformat(),
                'platform': 'Twitter Only',
                'debug_mode': self.debug,
                'content_stats': stats,
                'accounts': account_results
            }
            
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
            logger.info("🧪 运行测试模式")
            
            # 测试连接
            if bot.test_connections():
                print("✅ Twitter API连接测试通过")
            else:
                print("❌ Twitter API连接测试失败")
                return
            
            # 测试获取文章
            article = bot.get_next_article()
            if article:
                print(f"✅ 成功获取文章: {article.get('title', 'Unknown')}")
                print(f"📝 发布账号: {article.get('publish_account', 'default')}")
                print(f"👤 作者: {article.get('author', 'Unknown')}")
                print(f"📄 内容预览: {article.get('content', '')[:100]}...")
            else:
                print("❌ 无法获取文章")
        
        elif command == 'status':
            # 状态查看
            status = bot.get_status()
            print("📊 机器人状态:")
            print(f"  平台: {status.get('platform', 'Unknown')}")
            print(f"  调试模式: {status.get('debug_mode', False)}")
            
            stats = status.get('content_stats', {})
            if stats:
                print(f"📈 内容统计:")
                print(f"  总数: {stats.get('total', 0)}")
                print(f"  已发布: {stats.get('published', 0)}")
                print(f"  待发布: {stats.get('unpublished', 0)}")
            
            accounts = status.get('accounts', {})
            if accounts:
                print(f"🔗 账号状态:")
                for account, result in accounts.items():
                    status_icon = "✅" if result.get('status') == 'success' else "❌"
                    username = result.get('username', 'unknown')
                    print(f"  {status_icon} {account}: @{username}")
        
        elif command == 'run':
            # 执行一次发布
            logger.info("🚀 执行单次发布任务")
            success = bot.run_once()
            if success:
                print("✅ 发布任务完成")
            else:
                print("❌ 发布任务失败")
        
        elif command == 'schedule':
            # 定时任务模式（由GitHub Actions调用）
            bot.run_scheduled()
        
        else:
            print(f"❌ 未知命令: {command}")
            print("📋 可用命令:")
            print("  test     - 测试连接和获取文章")
            print("  status   - 查看机器人状态")
            print("  run      - 执行单次发布")
            print("  schedule - 定时任务模式")
    
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.error(f"程序运行时发生错误: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 