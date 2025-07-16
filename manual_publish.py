#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手动推文发布脚本
用于GitHub Actions工作流手动发布推文
"""

import os
import sys
import argparse
import logging
from datetime import datetime

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main_multi_account import MultiAccountTwitterPublisher


def setup_logging():
    """设置日志记录"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('manual_publish.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)


def validate_tweet_content(content):
    """验证推文内容"""
    if not content:
        raise ValueError("推文内容不能为空")
    
    if len(content) > 280:
        raise ValueError(f"推文内容超过280字符限制，当前长度：{len(content)}")
    
    return True


def validate_account(account):
    """验证账号名称"""
    valid_accounts = ['ContextSpace', 'OSS Discoveries', 'Ai flow watch', 'Open source reader']
    
    if account not in valid_accounts:
        raise ValueError(f"无效的账号名称：{account}。有效账号：{', '.join(valid_accounts)}")
    
    return True


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='手动发布Twitter推文')
    parser.add_argument('--content', required=True, help='推文内容')
    parser.add_argument('--account', required=True, help='目标账号')
    parser.add_argument('--debug', action='store_true', help='调试模式（不实际发布）')
    
    args = parser.parse_args()
    
    logger = setup_logging()
    
    try:
        # 验证输入
        validate_tweet_content(args.content)
        validate_account(args.account)
        
        logger.info("🚀 开始手动发布推文")
        logger.info(f"📄 推文内容: {args.content}")
        logger.info(f"📱 目标账号: {args.account}")
        logger.info(f"🐛 调试模式: {args.debug}")
        logger.info(f"⏰ 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if args.debug:
            logger.info("🐛 调试模式已启用 - 不会实际发布推文")
            logger.info("📝 推文预览：")
            logger.info(f"  账号: {args.account}")
            logger.info(f"  内容: {args.content}")
            logger.info("✅ 调试模式完成")
            return 0
        
        # 创建发布器
        publisher = MultiAccountTwitterPublisher()
        
        # 构建文章数据
        article_data = {
            'title': args.content[:50] + '...' if len(args.content) > 50 else args.content,
            'content': args.content,
            'author': '手动发布',
            'source': '手动发布',
            'publish_account': args.account,
            'published': '否',
            'is_published': False,
            '_source_file': 'manual_publish.py',
            '_row_index': 0,
            '_original_row': {}
        }
        
        logger.info(f"📤 发布推文到: {article_data['publish_account']}")
        logger.info(f"📝 推文内容: {article_data['content']}")
        
        # 发布推文
        success = publisher.publish_article(article_data)
        
        if success:
            logger.info("✅ 推文发布成功！")
            return 0
        else:
            logger.error("❌ 推文发布失败")
            return 1
            
    except Exception as e:
        logger.error(f"❌ 手动发布过程中发生错误: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 