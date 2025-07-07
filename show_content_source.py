#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv

print("📋 推文内容来源详情")
print("=" * 50)

try:
    with open('content_data.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    
    print(f"📄 数据源: content_data.csv")
    print(f"📊 总内容数: {len(data)}")
    
    published_count = 0
    unpublished_count = 0
    
    print(f"\n📚 内容列表:")
    for i, row in enumerate(data, 1):
        title = row.get('标题', 'Unknown')
        published = row.get('已发布', '').strip()
        
        if published == '是':
            status = "✅ 已发布"
            published_count += 1
        else:
            status = "⏳ 待发布"  
            unpublished_count += 1
            
        print(f"   {i}. {title} - {status}")
    
    print(f"\n📊 统计:")
    print(f"   已发布: {published_count}")
    print(f"   待发布: {unpublished_count}")
    
    # 显示下一篇要发布的内容
    for row in data:
        if row.get('已发布', '').strip() != '是':
            print(f"\n🚀 下次发布:")
            print(f"   标题: {row.get('标题', 'Unknown')}")
            print(f"   作者: {row.get('作者', 'Unknown')}")
            print(f"   来源: {row.get('来源', 'Unknown')}")
            break
    else:
        print(f"\n⚠️ 没有待发布内容")

except Exception as e:
    print(f"❌ 读取文件时出错: {e}") 