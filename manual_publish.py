#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitter手动发布脚本
支持单条推文立即发布，优化为只连接指定账号
"""

import sys
import logging
from datetime import datetime
from main_multi_account import MultiAccountTwitterPublisher

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('twitter_manual_publish.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def publish_single_tweet_manual(content: str, account: str = "ContextSpace") -> bool:
    """
    手动发布单条推文（单账号模式，不影响其他账号）
    
    Args:
        content: 推文内容
        account: 发布账号
        
    Returns:
        bool: 发布是否成功
    """
    try:
        logger.info("🚀 启动手动单条推文发布")
        logger.info("=" * 60)
        
        # 初始化发布器
        publisher = MultiAccountTwitterPublisher()
        
        # 使用单账号立即发布模式
        result = publisher.publish_single_tweet_only(content, account)
        
        # 输出结果
        logger.info("📊 发布结果:")
        logger.info("=" * 60)
        
        if result['success']:
            logger.info(f"✅ {result['message']}")
            logger.info(f"📍 账号: @{result['details'].get('username', 'unknown')}")
            logger.info(f"📝 内容: {result['details'].get('content', content[:50])}")
            return True
        else:
            logger.error(f"❌ {result['message']}")
            if 'error' in result['details']:
                logger.error(f"错误详情: {result['details']['error']}")
            return False
            
    except Exception as e:
        logger.error(f"💥 手动发布时发生异常: {str(e)}")
        return False

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("""
🐦 Twitter手动发布脚本使用方法:

python manual_publish.py "推文内容" [账号]

参数说明:
  推文内容: 要发布的推文文本（必需）
  账号: 发布账号，支持以下选项（可选，默认ContextSpace）:
    - ContextSpace 或 twitter (主账号)
    - OSS Discoveries 或 oss (开源工具账号)
    - Ai flow watch 或 ai (AI技术账号)  
    - Open source reader 或 reader (开源项目账号)

示例:
  python manual_publish.py "这是一条测试推文"
  python manual_publish.py "分享一个AI工具" "Ai flow watch"
  python manual_publish.py "推荐开源项目" "OSS Discoveries"

特点:
  ✅ 单账号模式 - 只连接指定账号，不影响其他账号
  ✅ 即时发布 - 立即发布到指定Twitter账号
  ✅ 详细日志 - 完整的发布过程和结果记录
        """)
        sys.exit(1)
    
    # 获取参数
    content = sys.argv[1]
    account = sys.argv[2] if len(sys.argv) > 2 else "ContextSpace"
    
    print(f"📝 推文内容: {content}")
    print(f"🎯 发布账号: {account}")
    print(f"🕒 发布时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    
    # 发布推文
    success = publish_single_tweet_manual(content, account)
    
    if success:
        print("\n🎉 推文发布成功！")
        sys.exit(0)
    else:
        print("\n❌ 推文发布失败！")
        sys.exit(1)

if __name__ == "__main__":
    main() 