#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Issue账号选择逻辑
"""

import re

def test_issue_account_selection():
    """测试Issue内容中的账号选择"""
    
    # 模拟Issue内容
    test_content = """**内容:** 这是一条测试推文，发布到Open source reader账号
**账号:** Open source reader"""
    
    print("🧪 测试Issue账号选择")
    print("=" * 50)
    print(f"测试内容:\n{test_content}")
    print("=" * 50)
    
    # 解析账号
    lines = test_content.split('\n')
    found_account = None
    
    for line in lines:
        line = line.strip()
        print(f"处理行: '{line}'")
        
        if line.startswith('**账号:**') or line.startswith('账号:'):
            account_text = line.split(':', 1)[1].strip()
            # 清理可能的星号
            account_text = account_text.lstrip('*').strip()
            found_account = account_text
            print(f"✅ 找到账号: '{account_text}'")
            break
    
    if found_account:
        # 账号映射
        account_lower = found_account.lower().strip()
        print(f"🔄 账号标准化: '{found_account}' -> '{account_lower}'")
        
        mapping = {
            'contextspace': 'ContextSpace',
            'context space': 'ContextSpace', 
            'twitter': 'ContextSpace',
            'oss discoveries': 'OSS Discoveries',
            'ossdiscoveries': 'OSS Discoveries',
            'oss': 'OSS Discoveries',
            'ai flow watch': 'Ai flow watch',
            'aiflowwatch': 'Ai flow watch', 
            'ai': 'Ai flow watch',
            'open source reader': 'Open source reader',
            'opensourcereader': 'Open source reader',
            'reader': 'Open source reader'
        }
        
        if account_lower in mapping:
            mapped_account = mapping[account_lower]
            print(f"✅ 映射成功: '{account_lower}' -> '{mapped_account}'")
        else:
            mapped_account = 'ContextSpace'
            print(f"❌ 映射失败: '{account_lower}' 不在映射表中，使用默认 ContextSpace")
        
        print(f"\n🎯 最终选择的账号: {mapped_account}")
    else:
        print("❌ 未找到账号信息")

if __name__ == "__main__":
    test_issue_account_selection() 