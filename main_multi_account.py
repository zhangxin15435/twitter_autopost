#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitter多账号自动发布系统
从content文件夹中的表格文件读取内容，并根据"发布账号"字段选择对应的Twitter账号发布
"""

import os
import csv
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional
from connect_twitter_multi import TwitterAccountManager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('twitter_multi_auto.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MultiAccountTwitterPublisher:
    """多账号Twitter发布器"""
    
    def __init__(self, content_folder: str = "content", excluded_accounts: List[str] = None):
        """
        初始化发布器
        
        Args:
            content_folder: 内容文件夹路径
            excluded_accounts: 暂时排除的账号列表
        """
        self.content_folder = content_folder
        self.account_manager = TwitterAccountManager()
        self.current_data = []
        
        # 暂时排除的账号列表
        self.excluded_accounts = excluded_accounts or []
        
        # 支持的文件格式
        self.supported_formats = ['.csv']
        
        if self.excluded_accounts:
            logger.info(f"多账号Twitter发布器初始化完成 (排除账号: {', '.join(self.excluded_accounts)})")
        else:
            logger.info(f"多账号Twitter发布器初始化完成")
    
    def publish_single_tweet(self, content: str, account_name: str) -> bool:
        """
        发布单条推文到指定账号
        
        Args:
            content: 推文内容
            account_name: 账号名称（如 'ContextSpace', 'OSS Discoveries' 等）
            
        Returns:
            bool: 发布是否成功
        """
        try:
            # 标准化账号名称
            account_mapping = {
                'contextspace': 'contextspace',
                'context space': 'contextspace', 
                'twitter': 'contextspace',
                'oss discoveries': 'ossdiscoveries',
                'ossdiscoveries': 'ossdiscoveries',
                'oss': 'ossdiscoveries',
                'ai flow watch': 'aiflowwatch',
                'aiflowwatch': 'aiflowwatch', 
                'ai': 'aiflowwatch',
                'open source reader': 'opensourcereader',
                'opensourcereader': 'opensourcereader',
                'reader': 'opensourcereader'
            }
            
            normalized_account = account_mapping.get(account_name.lower().strip(), 'contextspace')
            
            # 检查账号是否在排除列表中
            if normalized_account in self.excluded_accounts:
                logger.warning(f"账号 {normalized_account} 已被排除，跳过发布")
                return False
            
            # 获取API连接
            api = self.account_manager.get_api(normalized_account)
            if not api:
                logger.error(f"无法获取账号 {normalized_account} 的API连接")
                return False
            
            # 发布推文
            logger.info(f"正在发布推文到账号 {normalized_account}")
            logger.info(f"推文内容: {content[:50]}...")
            
            response = api.create_tweet(text=content)
            
            if response and response.data:
                tweet_id = response.data['id']
                logger.info(f"✅ 推文发布成功！Tweet ID: {tweet_id}")
                return True
            else:
                logger.error(f"❌ 推文发布失败，API响应异常")
                return False
                
        except Exception as e:
            logger.error(f"💥 发布推文时出现异常: {str(e)}")
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
                    'publish_account': source,  # 发布账号
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
    
    def get_next_articles_by_account(self) -> Dict[str, List[Dict]]:
        """按账号分组获取待发布的文章"""
        if not self.current_data:
            self.load_content_data()
        
        # 按账号分组
        articles_by_account = {}
        
        for article in self.current_data:
            if not article['is_published']:
                account = article['publish_account']
                if not account:
                    account = 'default'  # 默认账号
                
                # 检查是否在排除列表中
                if account in self.excluded_accounts:
                    logger.info(f"跳过排除账号: {account}")
                    continue
                
                if account not in articles_by_account:
                    articles_by_account[account] = []
                
                articles_by_account[account].append(article)
        
        return articles_by_account
    
    def get_next_article(self) -> Optional[Dict]:
        """获取下一篇待发布的文章"""
        if not self.current_data:
            self.load_content_data()
        
        # 查找未发布的文章
        for article in self.current_data:
            if not article['is_published']:
                account = article['publish_account']
                if not account:
                    account = 'default'
                
                # 检查是否在排除列表中
                if account in self.excluded_accounts:
                    logger.info(f"跳过排除账号: {account}")
                    continue
                
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
        """发布文章到对应的Twitter账号"""
        try:
            # 获取发布账号
            publish_account = article['publish_account']
            if not publish_account:
                publish_account = 'default'
            
            logger.info(f"准备发布到账号: {publish_account}")
            
            # 格式化推文内容
            tweet_content = self.format_tweet_content(article)
            
            logger.info(f"准备发布推文: {tweet_content[:100]}...")
            
            # 发布推文
            result = self.account_manager.publish_tweet(publish_account, tweet_content)
            
            if result and result.get('id'):
                tweet_id = result.get('id')
                username = result.get('username', 'unknown')
                tweet_url = result.get('url', '')
                
                logger.info(f"🎉 推文发布成功！")
                logger.info(f"   账号: @{username}")
                logger.info(f"   推文ID: {tweet_id}")
                logger.info(f"   链接: {tweet_url}")
                
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
        
        stats = {
            'total': len(self.current_data),
            'published': sum(1 for article in self.current_data if article['is_published']),
            'unpublished': 0,
            'by_account': {},
            'excluded_accounts': self.excluded_accounts
        }
        
        stats['unpublished'] = stats['total'] - stats['published']
        
        # 按账号统计
        for article in self.current_data:
            account = article['publish_account'] or 'default'
            
            if account not in stats['by_account']:
                stats['by_account'][account] = {
                    'total': 0,
                    'published': 0,
                    'unpublished': 0,
                    'excluded': account in self.excluded_accounts
                }
            
            stats['by_account'][account]['total'] += 1
            if article['is_published']:
                stats['by_account'][account]['published'] += 1
            else:
                stats['by_account'][account]['unpublished'] += 1
        
        return stats
    
    def test_all_accounts(self) -> Dict:
        """测试所有账号的连接状态"""
        return self.account_manager.test_all_accounts()
    
    def run_once(self) -> bool:
        """运行一次发布任务"""
        try:
            logger.info("🚀 开始执行多账号发布任务")
            
            # 测试账号连接
            account_results = self.test_all_accounts()
            logger.info("📋 账号连接状态:")
            for account_name, result in account_results.items():
                if result['status'] == 'success':
                    logger.info(f"   ✅ {account_name} (@{result['username']})")
                else:
                    logger.warning(f"   ❌ {account_name} - {result.get('error', '未知错误')}")
            
            # 获取统计信息
            stats = self.get_statistics()
            logger.info(f"📊 内容统计:")
            logger.info(f"   总数: {stats['total']}")
            logger.info(f"   已发布: {stats['published']}")
            logger.info(f"   未发布: {stats['unpublished']}")
            
            # 按账号显示统计
            for account, account_stats in stats['by_account'].items():
                if account_stats.get('excluded', False):
                    logger.info(f"   {account}: {account_stats['unpublished']} 待发布 (已暂停)")
                else:
                    logger.info(f"   {account}: {account_stats['unpublished']} 待发布")
            
            # 获取下一篇文章
            article = self.get_next_article()
            
            if not article:
                logger.info("✅ 没有待发布的文章")
                return True
            
            logger.info(f"📝 准备发布: {article['title']}")
            logger.info(f"👤 作者: {article['author']}")
            logger.info(f"📍 发布账号: {article['publish_account']}")
            
            # 发布文章
            success = self.publish_article(article)
            
            if success:
                logger.info("🎉 多账号发布任务完成")
            else:
                logger.error("❌ 多账号发布任务失败")
            
            return success
            
        except Exception as e:
            logger.error(f"运行发布任务时发生错误: {str(e)}")
            return False
    
    def run_batch(self, max_posts: int = 5) -> Dict:
        """批量运行发布任务"""
        try:
            logger.info(f"🚀 开始批量发布任务 (最多 {max_posts} 篇)")
            
            results = {
                'success': 0,
                'failed': 0,
                'total': 0,
                'details': []
            }
            
            # 按账号分组获取文章
            articles_by_account = self.get_next_articles_by_account()
            
            if not articles_by_account:
                logger.info("✅ 没有待发布的文章")
                return results
            
            # 为每个账号发布一篇文章
            for account, articles in articles_by_account.items():
                if results['total'] >= max_posts:
                    break
                
                if not articles:
                    continue
                
                article = articles[0]  # 取第一篇
                
                logger.info(f"📝 发布到账号 '{account}': {article['title']}")
                
                success = self.publish_article(article)
                
                result_detail = {
                    'account': account,
                    'title': article['title'],
                    'success': success
                }
                
                results['details'].append(result_detail)
                results['total'] += 1
                
                if success:
                    results['success'] += 1
                else:
                    results['failed'] += 1
                
                # 添加延迟避免API限制
                time.sleep(2)
            
            logger.info(f"🎉 批量发布完成: {results['success']} 成功, {results['failed']} 失败")
            
            return results
            
        except Exception as e:
            logger.error(f"批量发布时发生错误: {str(e)}")
            return {'success': 0, 'failed': 0, 'total': 0, 'details': []}

def main():
    """主函数"""
    print("🚀 Twitter多账号自动发布系统")
    print("=" * 50)
    
    try:
        # 暂时排除contextspace账号的自动发布
        excluded_accounts = ['ContextSpace']
        
        # 创建发布器
        publisher = MultiAccountTwitterPublisher(excluded_accounts=excluded_accounts)
        
        # 运行一次
        success = publisher.run_once()
        
        if success:
            print("✅ 多账号发布任务完成")
        else:
            print("❌ 多账号发布任务失败")
            
    except Exception as e:
        print(f"❌ 程序执行失败: {str(e)}")
        logger.error(f"程序执行失败: {str(e)}")

if __name__ == "__main__":
    main() 