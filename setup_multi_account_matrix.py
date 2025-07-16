#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitter多账号矩阵设置向导
帮助用户配置和测试多账号发布系统
"""

import os
import logging
from typing import Dict, List
from connect_twitter_multi import TwitterAccountManager, MultiTwitterAPI

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MultiAccountMatrixSetup:
    """多账号矩阵设置向导"""
    
    def __init__(self):
        self.account_manager = TwitterAccountManager()
        self.recommended_accounts = {
            'contextspace': {
                'display_name': '@ContextSpace',
                'description': '主账号，综合内容发布',
                'target_audience': '综合受众、订阅用户',
                'content_types': ['twitter', 'contextspace', '综合内容'],
                'posting_frequency': '每日2-3条',
                'best_time': '每天 20:00-22:00'
            },
            'ossdiscoveries': {
                'display_name': '@OSSDiscoveries',
                'description': '开源工具发现、设计工具',
                'target_audience': '设计师、工具用户、开发者',
                'content_types': ['oss discoveries'],
                'posting_frequency': '每日1条',
                'best_time': '周末 10:00-12:00'
            },
            'aiflowwatch': {
                'display_name': '@AIFlowWatch',
                'description': 'AI技术、机器学习、工作流',
                'target_audience': 'AI开发者、技术专家',
                'content_types': ['ai flow watch'],
                'posting_frequency': '每日1-2条',
                'best_time': '工作日 09:00-11:00'
            },
            'opensourcereader': {
                'display_name': '@OpenSourceReader',
                'description': '开源项目介绍、技术评测、文档解读',
                'target_audience': '开发者、开源贡献者、技术阅读者',
                'content_types': ['open source reader'],
                'posting_frequency': '每日1条',
                'best_time': '工作日 14:00-16:00'
            }
        }
    
    def display_welcome(self):
        """显示欢迎信息"""
        print("🚀 Twitter多账号矩阵设置向导")
        print("=" * 60)
        print("📊 基于您的内容分析，推荐以下专业账号矩阵：")
        print()
        
        for account_key, info in self.recommended_accounts.items():
            print(f"📱 {info['display_name']}")
            print(f"   🎯 定位: {info['description']}")
            print(f"   👥 受众: {info['target_audience']}")
            print(f"   📝 内容: {', '.join(info['content_types'])}")
            print(f"   ⏰ 发布: {info['posting_frequency']} ({info['best_time']})")
            print()
    
    def check_current_config(self) -> Dict:
        """检查当前配置状态"""
        print("🔍 检查当前API配置状态...")
        print("-" * 40)
        
        results = self.account_manager.test_all_accounts()
        
        configured_accounts = []
        missing_accounts = []
        
        for account_key in self.recommended_accounts.keys():
            if account_key in results and results[account_key]['status'] == 'success':
                username = results[account_key]['username']
                print(f"✅ {account_key}: @{username}")
                configured_accounts.append(account_key)
            else:
                print(f"❌ {account_key}: 配置缺失")
                missing_accounts.append(account_key)
        
        print()
        print(f"📊 配置状态: {len(configured_accounts)}/{len(self.recommended_accounts)} 个账号已配置")
        
        return {
            'configured': configured_accounts,
            'missing': missing_accounts,
            'total': len(self.recommended_accounts),
            'ready': len(configured_accounts)
        }
    
    def show_content_distribution(self):
        """显示内容分布情况"""
        print("📈 当前内容分布分析")
        print("-" * 40)
        
        try:
            from main_multi_account import MultiAccountTwitterPublisher
            publisher = MultiAccountTwitterPublisher()
            stats = publisher.get_statistics()
            
            print(f"📊 总体统计:")
            print(f"   总内容数: {stats['total']}")
            print(f"   已发布: {stats['published']}")
            print(f"   待发布: {stats['unpublished']}")
            print()
            
            print(f"📝 按账号分布:")
            for account, data in stats['by_account'].items():
                account_info = self.recommended_accounts.get(account, {})
                display_name = account_info.get('display_name', account)
                print(f"   {display_name}: {data['unpublished']} 待发布")
            
        except Exception as e:
            print(f"⚠️ 无法获取内容统计: {str(e)}")
        
        print()
    
    def generate_config_template(self, missing_accounts: List[str]):
        """生成配置模板"""
        if not missing_accounts:
            return
        
        print("📝 生成四个账号配置模板")
        print("-" * 40)
        print("请将以下配置添加到您的 .env 文件或 GitHub Secrets：")
        print()
        
        account_configs = {
            'contextspace': {
                'name': 'ContextSpace主账号',
                'prefix': 'CONTEXTSPACE'
            },
            'ossdiscoveries': {
                'name': 'OSS Discoveries账号',
                'prefix': 'OSSDISCOVERIES'
            },
            'aiflowwatch': {
                'name': 'AI Flow Watch账号',
                'prefix': 'AIFLOWWATCH'
            },
            'opensourcereader': {
                'name': 'Open Source Reader账号',
                'prefix': 'OPENSOURCEREADER'
            }
        }
        
        for account in missing_accounts:
            if account in account_configs:
                config = account_configs[account]
                print(f"# {config['name']}")
                print(f"TWITTER_{config['prefix']}_CONSUMER_KEY={account}_consumer_key")
                print(f"TWITTER_{config['prefix']}_CONSUMER_SECRET={account}_consumer_secret")
                print(f"TWITTER_{config['prefix']}_ACCESS_TOKEN={account}_access_token")
                print(f"TWITTER_{config['prefix']}_ACCESS_TOKEN_SECRET={account}_access_token_secret")
                print(f"TWITTER_{config['prefix']}_BEARER_TOKEN={account}_bearer_token")
                print()
    
    def test_single_account_mode(self):
        """测试单账号模式"""
        print("🧪 测试单账号模式（当前推荐）")
        print("-" * 40)
        
        try:
            from main_multi_account import MultiAccountTwitterPublisher
            publisher = MultiAccountTwitterPublisher()
            
            # 获取下一篇待发布文章
            article = publisher.get_next_article()
            
            if article:
                print(f"📝 下一篇待发布:")
                print(f"   标题: {article['title']}")
                print(f"   作者: {article['author']}")
                print(f"   发布账号: {article['publish_account']}")
                print(f"   内容: {article['content'][:100]}...")
                print()
                
                response = input("是否现在发布这篇内容？(y/n): ").strip().lower()
                if response == 'y':
                    print("🚀 正在发布...")
                    success = publisher.publish_article(article)
                    if success:
                        print("✅ 发布成功！")
                    else:
                        print("❌ 发布失败")
                else:
                    print("⏸️ 跳过发布")
            else:
                print("ℹ️ 当前没有待发布的内容")
                
        except Exception as e:
            print(f"❌ 测试失败: {str(e)}")
    
    def show_next_steps(self, config_status: Dict):
        """显示后续步骤"""
        print("🎯 下一步建议")
        print("-" * 40)
        
        if config_status['ready'] == 0:
            print("1. 📋 配置至少一个Twitter账号API密钥")
            print("2. 🧪 测试基本发布功能")
            print("3. 📊 分析内容分布情况")
            print("4. 🚀 开始单账号发布")
            
        elif config_status['ready'] == 1:
            print("✅ 单账号模式已就绪！")
            print("1. 🚀 开始使用单账号发布内容")
            print("2. 📈 观察发布效果和受众反馈")
            print("3. 💰 如有需要，申请更多Twitter账号API")
            print("4. 🔄 逐步扩展到多账号矩阵")
            
        else:
            print("🎉 多账号矩阵已配置！")
            print("1. 🧪 测试所有账号的发布功能")
            print("2. ⏰ 设置不同账号的发布时间")
            print("3. 📊 监控各账号的表现数据")
            print("4. 🔄 优化内容策略和发布频率")
        
        print()
        print("💡 快速开始命令:")
        print("   python main_multi_account.py          # 发布一篇内容")
        print("   python connect_twitter_multi.py       # 测试账号连接")
        print("   python setup_multi_account_matrix.py  # 重新运行设置向导")
        
    def run_setup_wizard(self):
        """运行设置向导"""
        # 显示欢迎信息
        self.display_welcome()
        
        # 检查当前配置
        config_status = self.check_current_config()
        
        # 显示内容分布
        self.show_content_distribution()
        
        # 生成配置模板
        if config_status['missing']:
            self.generate_config_template(config_status['missing'])
        
        # 如果有可用配置，提供测试选项
        if config_status['configured']:
            print("🎮 测试选项")
            print("-" * 40)
            
            response = input("是否要测试当前配置的发布功能？(y/n): ").strip().lower()
            if response == 'y':
                self.test_single_account_mode()
                print()
        
        # 显示后续步骤
        self.show_next_steps(config_status)

def main():
    """主函数"""
    try:
        setup = MultiAccountMatrixSetup()
        setup.run_setup_wizard()
        
    except KeyboardInterrupt:
        print("\n\n👋 设置向导已停止")
    except Exception as e:
        print(f"\n❌ 设置向导出错: {str(e)}")

if __name__ == "__main__":
    main() 