#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitter自动发布主程序 - CSV数据源版本
立即可用的解决方案
"""

import os
import logging
from datetime import datetime, timezone
from connect_twitter import TwitterAPI
from connect_csv import CSVDataSource

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('twitter_publish.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def format_tweet_content(article: dict) -> str:
    """格式化推文内容"""
    title = article.get('title', '').strip()
    content = article.get('content', '').strip()
    author = article.get('author', '').strip()
    source = article.get('source', '').strip()
    
    # 智能内容截取和格式化
    tweet_content = f"📢 {title}\n\n"
    
    # 计算剩余字符数（考虑标题、换行符等）
    remaining_chars = 280 - len(tweet_content) - 50  # 预留50字符给作者和来源信息
    
    # 处理内容
    if len(content) > remaining_chars:
        # 截取内容，确保在句子末尾截断
        truncated_content = content[:remaining_chars]
        last_period = max(
            truncated_content.rfind('。'),
            truncated_content.rfind('！'),
            truncated_content.rfind('？'),
            truncated_content.rfind('.'),
            truncated_content.rfind('!'),
            truncated_content.rfind('?')
        )
        
        if last_period > remaining_chars * 0.7:  # 如果截断点不太靠前
            content = truncated_content[:last_period + 1]
        else:
            content = truncated_content + "..."
    
    tweet_content += content
    
    # 添加作者和来源信息
    footer_parts = []
    if author:
        footer_parts.append(f"👤 {author}")
    if source:
        footer_parts.append(f"📝 {source}")
    
    if footer_parts:
        footer = f"\n\n{' | '.join(footer_parts)}"
        
        # 确保总长度不超过280字符
        if len(tweet_content + footer) <= 280:
            tweet_content += footer
    
    return tweet_content

def publish_content():
    """发布内容到Twitter"""
    logging.info("开始执行Twitter自动发布任务")
    print(f"🚀 Twitter自动发布系统启动 - CSV数据源版本")
    print(f"⏰ 执行时间: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"=" * 60)
    
    try:
        # 初始化Twitter API
        twitter_api = TwitterAPI()
        print(f"✅ Twitter API连接成功")
        
        # 初始化CSV数据源
        csv_source = CSVDataSource()
        print(f"✅ CSV数据源连接成功")
        
        # 获取内容统计
        stats = csv_source.get_statistics()
        print(f"\n📊 内容库状态:")
        print(f"   总内容数: {stats['total']}")
        print(f"   已发布: {stats['published']}")
        print(f"   待发布: {stats['unpublished']}")
        
        # 获取未发布的文章
        article = csv_source.get_article_content()
        
        if not article:
            logging.info("没有找到未发布的内容")
            print(f"\n⚠️ 没有找到未发布的内容")
            print(f"💡 建议:")
            print(f"   1. 检查 content_data.csv 文件")
            print(f"   2. 确保有内容标记为未发布")
            print(f"   3. 添加新内容到CSV文件")
            return False
        
        # 显示即将发布的内容
        print(f"\n📝 即将发布的内容:")
        print(f"   标题: {article['title']}")
        print(f"   作者: {article['author']}")
        print(f"   来源: {article['source']}")
        print(f"   内容长度: {len(article['content'])} 字符")
        
        # 格式化推文内容
        tweet_content = format_tweet_content(article)
        print(f"\n🔧 格式化后的推文:")
        print(f"{'='*40}")
        print(tweet_content)
        print(f"{'='*40}")
        print(f"推文长度: {len(tweet_content)} 字符")
        
        # 发布到Twitter
        print(f"\n🚀 正在发布到Twitter...")
        tweet_result = twitter_api.create_tweet(tweet_content)
        
        if tweet_result:
            # 标记为已发布
            csv_source.mark_as_published(article['_row_index'])
            
            # 记录成功
            logging.info(f"成功发布推文: {article['title']}")
            print(f"✅ 发布成功!")
            print(f"🔗 推文ID: {tweet_result.get('id')}")
            print(f"📝 推文内容: {tweet_result.get('text', '')[:50]}...")
            
            # 更新后的统计
            new_stats = csv_source.get_statistics()
            print(f"\n📊 更新后状态:")
            print(f"   已发布: {new_stats['published']}")
            print(f"   待发布: {new_stats['unpublished']}")
            
            return True
            
        else:
            logging.error("推文发布失败")
            print(f"❌ 推文发布失败")
            return False
            
    except Exception as e:
        error_msg = f"发布过程中发生错误: {str(e)}"
        logging.error(error_msg)
        print(f"❌ {error_msg}")
        return False

def verify_configuration():
    """验证系统配置"""
    print(f"🔍 验证系统配置...")
    
    # 检查Twitter API配置
    twitter_env_vars = [
        'TWITTER_CONSUMER_KEY',
        'TWITTER_CONSUMER_SECRET', 
        'TWITTER_ACCESS_TOKEN',
        'TWITTER_ACCESS_TOKEN_SECRET'
    ]
    
    missing_vars = []
    for var in twitter_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ 缺少Twitter API环境变量: {missing_vars}")
        print(f"💡 请设置以下环境变量:")
        for var in missing_vars:
            print(f"   {var}=your_value")
        return False
    
    print(f"✅ Twitter API配置完整")
    
    # 检查CSV文件
    if not os.path.exists('content_data.csv'):
        print(f"⚠️ content_data.csv 文件不存在，将自动创建")
    else:
        print(f"✅ CSV数据文件存在")
    
    return True

def show_usage_guide():
    """显示使用指南"""
    print(f"\n📚 CSV数据源使用指南:")
    print(f"=" * 60)
    print(f"1. 📄 编辑 content_data.csv 文件")
    print(f"2. 📝 添加要发布的内容:")
    print(f"   - 标题: 推文的主标题")
    print(f"   - 内容: 详细内容") 
    print(f"   - 作者: 内容作者")
    print(f"   - 来源: 内容来源")
    print(f"   - 已发布: 设为'否'表示未发布")
    print(f"3. 🚀 运行发布程序")
    print(f"4. ✅ 系统会自动选择未发布内容并发布")
    print(f"5. 🔄 发布后内容会自动标记为已发布")
    
    print(f"\n📋 示例CSV格式:")
    print(f"标题,内容,作者,来源,已发布")
    print(f"AI技术趋势,人工智能发展迅速...,技术专家,科技新闻,否")
    
    print(f"\n🔧 高级功能:")
    print(f"• 智能内容截取 - 自动适配280字符限制")
    print(f"• 状态管理 - 防止重复发布")
    print(f"• 错误处理 - 详细日志记录")
    print(f"• 内容统计 - 发布状态追踪")

def main():
    """主函数"""
    print(f"🎯 Twitter自动发布系统 - CSV数据源版本")
    print(f"⚡ 立即可用的解决方案")
    print(f"🔗 https://github.com/your-repo/twitter-auto")
    print(f"=" * 60)
    
    # 验证配置
    if not verify_configuration():
        print(f"\n❌ 配置验证失败，请检查配置后重试")
        show_usage_guide()
        return
    
    print(f"✅ 系统配置验证通过")
    
    # 执行发布
    success = publish_content()
    
    if success:
        print(f"\n🎉 发布任务执行成功!")
        print(f"📅 下次发布时间请查看GitHub Actions调度")
    else:
        print(f"\n⚠️ 发布任务执行完成，但没有内容发布")
        show_usage_guide()
    
    print(f"\n" + "=" * 60)
    print(f"🎯 Twitter自动发布系统执行完毕")

if __name__ == "__main__":
    main() 