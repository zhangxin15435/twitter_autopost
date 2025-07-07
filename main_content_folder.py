#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitter自动发布系统 - Content文件夹版本
从content文件夹中的表格文件读取内容并发布到Twitter
"""

import os
import csv
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional
from connect_twitter import TwitterAPI

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('twitter_auto.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ContentFolderTwitterPublisher:
    """Content文件夹Twitter发布器"""
    
    def __init__(self, content_folder: str = "content"):
        """初始化发布器"""
        self.content_folder = content_folder
        self.twitter_api = None
        self.current_data = []
        
        # 支持的文件格式
        self.supported_formats = ['.csv']
        
        logger.info(f"Content文件夹Twitter发布器初始化完成")
    
    def connect_twitter(self) -> bool:
        """连接Twitter API"""
        try:
            self.twitter_api = TwitterAPI()
            
            # 测试连接
            if self.twitter_api.test_connection():
                logger.info(f"✅ Twitter API连接成功")
                return True
            else:
                logger.error("❌ Twitter API连接失败")
                return False
                
        except Exception as e:
            logger.error(f"❌ Twitter API连接错误: {str(e)}")
            return False
    
    def load_content_data(self) -> List[Dict]:
        """加载content文件夹中的数据"""
        try:
            # 查找CSV文件
            csv_files = []
            for file in os.listdir(self.content_folder):
                if file.endswith('.csv'):
                    csv_files.append(os.path.join(self.content_folder, file))
            
            if not csv_files:
                logger.warning("在content文件夹中没有找到CSV文件")
                return []
            
            logger.info(f"找到 {len(csv_files)} 个CSV文件")
            
            all_data = []
            for csv_file in csv_files:
                logger.info(f"读取文件: {os.path.basename(csv_file)}")
                
                try:
                    # 尝试不同编码
                    encodings = ['utf-8', 'utf-8-sig', 'gbk', 'gb2312']
                    data = None
                    
                    for encoding in encodings:
                        try:
                            with open(csv_file, 'r', encoding=encoding) as f:
                                reader = csv.DictReader(f)
                                data = list(reader)
                                logger.info(f"成功使用编码 {encoding} 读取 {len(data)} 行数据")
                                break
                        except Exception:
                            continue
                    
                    if not data:
                        logger.error(f"无法读取文件 {csv_file}")
                        continue
                    
                    # 处理数据
                    processed_data = self.process_csv_data(data, csv_file)
                    all_data.extend(processed_data)
                    
                except Exception as e:
                    logger.error(f"处理文件 {csv_file} 时发生错误: {str(e)}")
            
            self.current_data = all_data
            logger.info(f"总共加载 {len(all_data)} 条有效数据")
            return all_data
            
        except Exception as e:
            logger.error(f"加载数据时发生错误: {str(e)}")
            return []
    
    def process_csv_data(self, raw_data: List[Dict], file_path: str) -> List[Dict]:
        """处理CSV数据"""
        processed_data = []
        
        for i, row in enumerate(raw_data):
            try:
                # 获取内容主题（可能包含引号）
                content = ""
                for field_name in row.keys():
                    if '内容主题' in field_name:  # 匹配包含"内容主题"的字段
                        content = row[field_name]
                        break
                
                if not content or not content.strip():
                    continue
                
                # 获取其他字段
                author = row.get('提出人', '').strip()
                source = row.get('发布账号', '').strip()
                publish_status = row.get('是否发布', '').strip()
                
                # 创建标准格式的数据
                processed_row = {
                    'title': content[:50] + "..." if len(content) > 50 else content,
                    'content': content.strip(),
                    'author': author,
                    'source': source,
                    'published': publish_status,
                    'is_published': publish_status.lower() in ['是', 'yes', 'true', '1'],
                    '_source_file': file_path,
                    '_row_index': i,
                    '_original_row': row
                }
                
                processed_data.append(processed_row)
                
            except Exception as e:
                logger.error(f"处理第 {i+1} 行数据时发生错误: {str(e)}")
        
        logger.info(f"从 {os.path.basename(file_path)} 处理了 {len(processed_data)} 条有效数据")
        return processed_data
    
    def get_next_article(self) -> Optional[Dict]:
        """获取下一篇待发布的文章"""
        if not self.current_data:
            self.load_content_data()
        
        # 查找未发布的文章
        for article in self.current_data:
            if not article['is_published']:
                return article
        
        return None
    
    def format_tweet_content(self, article: Dict) -> str:
        """格式化推文内容"""
        content = article['content']
        
        # 如果内容超过Twitter字符限制，进行截断
        max_length = 280
        if len(content) > max_length:
            content = content[:max_length-3] + "..."
        
        return content
    
    def publish_article(self, article: Dict) -> bool:
        """发布文章到Twitter"""
        try:
            if not self.twitter_api:
                logger.error("Twitter API未连接")
                return False
            
            # 格式化推文内容
            tweet_content = self.format_tweet_content(article)
            
            logger.info(f"准备发布推文: {tweet_content[:100]}...")
            
            # 发布推文
            result = self.twitter_api.create_tweet(tweet_content)
            
            if result and result.get('id'):
                tweet_id = result.get('id')
                logger.info(f"🎉 推文发布成功！推文ID: {tweet_id}")
                
                # 标记为已发布
                if self.mark_as_published(article):
                    logger.info("✅ 文章状态更新成功")
                else:
                    logger.warning("⚠️ 文章状态更新失败")
                
                return True
            else:
                logger.error(f"❌ 推文发布失败")
                return False
                
        except Exception as e:
            logger.error(f"发布文章时发生错误: {str(e)}")
            return False
    
    def mark_as_published(self, article: Dict) -> bool:
        """标记文章为已发布"""
        try:
            source_file = article['_source_file']
            row_index = article['_row_index']
            
            # 读取原始文件
            with open(source_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                fieldnames = reader.fieldnames
            
            # 找到发布状态字段
            status_field = None
            for field in fieldnames:
                if '是否发布' in field:
                    status_field = field
                    break
            
            if not status_field:
                logger.error("未找到发布状态字段")
                return False
            
            # 更新状态
            if row_index < len(rows):
                rows[row_index][status_field] = '是'
                
                # 写回文件
                with open(source_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)
                
                # 更新内存中的数据
                article['is_published'] = True
                article['published'] = '是'
                
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"标记已发布时发生错误: {str(e)}")
            return False
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        if not self.current_data:
            self.load_content_data()
        
        total = len(self.current_data)
        published = sum(1 for article in self.current_data if article['is_published'])
        unpublished = total - published
        
        return {
            'total': total,
            'published': published,
            'unpublished': unpublished
        }
    
    def run_once(self) -> bool:
        """运行一次发布任务"""
        try:
            logger.info("🚀 开始执行发布任务")
            
            # 连接Twitter
            if not self.connect_twitter():
                return False
            
            # 获取统计信息
            stats = self.get_statistics()
            logger.info(f"📊 内容统计: 总数={stats['total']}, 已发布={stats['published']}, 未发布={stats['unpublished']}")
            
            # 获取下一篇文章
            article = self.get_next_article()
            
            if not article:
                logger.info("✅ 没有待发布的文章")
                return True
            
            logger.info(f"📝 准备发布: {article['title']}")
            logger.info(f"👤 作者: {article['author']}")
            logger.info(f"📍 来源: {article['source']}")
            
            # 发布文章
            success = self.publish_article(article)
            
            if success:
                logger.info("🎉 发布任务完成")
            else:
                logger.error("❌ 发布任务失败")
            
            return success
            
        except Exception as e:
            logger.error(f"运行发布任务时发生错误: {str(e)}")
            return False

def main():
    """主函数"""
    print("🚀 Twitter自动发布系统 - Content文件夹版本")
    print("=" * 50)
    
    try:
        # 创建发布器
        publisher = ContentFolderTwitterPublisher()
        
        # 运行一次
        success = publisher.run_once()
        
        if success:
            print("✅ 发布任务完成")
        else:
            print("❌ 发布任务失败")
            
    except Exception as e:
        print(f"❌ 程序执行失败: {str(e)}")
        logger.error(f"程序执行失败: {str(e)}")

if __name__ == "__main__":
    main() 