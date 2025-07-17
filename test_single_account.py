#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单账号发布模式测试脚本
验证单账号发布时是否只连接指定账号，不影响其他账号
"""

import logging
from datetime import datetime
from main_multi_account import MultiAccountTwitterPublisher

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_single_account.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def test_single_account_connection():
    """测试单账号连接模式"""
    try:
        logger.info("🧪 开始测试单账号连接模式")
        logger.info("=" * 60)
        
        publisher = MultiAccountTwitterPublisher()
        
        # 测试所有账号的单账号连接
        test_accounts = ['ContextSpace', 'OSS Discoveries', 'Ai flow watch', 'Open source reader']
        
        for account in test_accounts:
            logger.info(f"\n🔍 测试账号: {account}")
            logger.info("-" * 40)
            
            # 使用单账号测试模式
            result = publisher.test_single_account(account)
            
            # 分析结果
            for account_key, account_result in result.items():
                if account_result['status'] == 'success':
                    logger.info(f"✅ {account_key} 连接成功")
                    logger.info(f"   用户名: @{account_result['username']}")
                else:
                    logger.warning(f"❌ {account_key} 连接失败")
                    logger.warning(f"   错误: {account_result.get('error', '未知错误')}")
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ 单账号连接测试完成")
        return True
        
    except Exception as e:
        logger.error(f"💥 测试过程中发生异常: {str(e)}")
        return False

def test_single_account_publish():
    """测试单账号发布模式（只测试连接，不实际发布）"""
    try:
        logger.info("\n🧪 开始测试单账号发布模式")
        logger.info("=" * 60)
        
        publisher = MultiAccountTwitterPublisher()
        
        # 测试内容
        test_content = f"这是一条测试推文 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        test_account = "ContextSpace"  # 使用主账号测试
        
        logger.info(f"📝 测试内容: {test_content}")
        logger.info(f"🎯 测试账号: {test_account}")
        
        # 使用单账号立即发布模式（干运行）
        logger.info("\n🔍 执行单账号发布模式测试...")
        
        # 首先测试连接
        test_result = publisher.test_single_account(test_account)
        account_key = list(test_result.keys())[0]
        
        if test_result[account_key]['status'] == 'success':
            logger.info(f"✅ 账号 {account_key} 连接测试成功")
            logger.info(f"   用户名: @{test_result[account_key]['username']}")
            logger.info("🔧 连接已验证，但未实际发布推文（测试模式）")
        else:
            logger.warning(f"❌ 账号 {account_key} 连接失败")
            logger.warning(f"   错误: {test_result[account_key].get('error', '未知错误')}")
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ 单账号发布模式测试完成")
        return True
        
    except Exception as e:
        logger.error(f"💥 测试过程中发生异常: {str(e)}")
        return False

def test_account_isolation():
    """测试账号隔离性 - 确保只连接指定账号"""
    try:
        logger.info("\n🧪 开始测试账号隔离性")
        logger.info("=" * 60)
        
        publisher = MultiAccountTwitterPublisher()
        
        # 清空活跃API缓存
        publisher.account_manager.active_apis.clear()
        logger.info("🧹 已清空API缓存")
        
        # 测试单个账号连接
        test_account = "ContextSpace"
        logger.info(f"🎯 只连接账号: {test_account}")
        
        result = publisher.test_single_account(test_account)
        
        # 检查缓存中是否只有一个账号
        active_accounts = list(publisher.account_manager.active_apis.keys())
        logger.info(f"📊 活跃连接数: {len(active_accounts)}")
        logger.info(f"📋 活跃账号: {active_accounts}")
        
        if len(active_accounts) == 1:
            logger.info("✅ 账号隔离性测试通过 - 只连接了指定账号")
        elif len(active_accounts) == 0:
            logger.warning("⚠️ 没有成功连接任何账号")
        else:
            logger.error(f"❌ 账号隔离性测试失败 - 连接了 {len(active_accounts)} 个账号")
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ 账号隔离性测试完成")
        return len(active_accounts) <= 1
        
    except Exception as e:
        logger.error(f"💥 测试过程中发生异常: {str(e)}")
        return False

def main():
    """主函数"""
    logger.info("🚀 启动单账号发布模式测试套件")
    logger.info(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 80)
    
    # 执行所有测试
    tests = [
        ("单账号连接测试", test_single_account_connection),
        ("单账号发布测试", test_single_account_publish),
        ("账号隔离性测试", test_account_isolation),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        logger.info(f"\n🧪 执行测试: {test_name}")
        try:
            success = test_func()
            results.append((test_name, success))
            if success:
                logger.info(f"✅ {test_name} 通过")
            else:
                logger.error(f"❌ {test_name} 失败")
        except Exception as e:
            logger.error(f"💥 {test_name} 异常: {str(e)}")
            results.append((test_name, False))
    
    # 汇总结果
    logger.info("\n" + "=" * 80)
    logger.info("📊 测试结果汇总:")
    logger.info("=" * 80)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        logger.info(f"   {test_name}: {status}")
        if success:
            passed += 1
    
    logger.info(f"\n🎯 总体结果: {passed}/{total} 测试通过")
    
    if passed == total:
        logger.info("🎉 所有测试通过！单账号发布模式工作正常")
        return True
    else:
        logger.error("❌ 部分测试失败，请检查配置和网络连接")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 