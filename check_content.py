#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查CSV内容状态
"""

from connect_csv import CSVDataSource

def check_content_status():
    """检查内容状态"""
    print("📊 当前内容状态检查")
    print("=" * 40)
    
    csv_source = CSVDataSource()
    
    # 获取统计信息
    stats = csv_source.get_statistics()
    print(f"📋 内容统计:")
    print(f"   总数: {stats['total']}")
    print(f"   已发布: {stats['published']}")
    print(f"   待发布: {stats['unpublished']}")
    
    # 获取下一篇待发布内容
    article = csv_source.get_article_content()
    
    if article:
        print(f"\n📝 下一篇待发布:")
        print(f"   标题: {article['title']}")
        print(f"   作者: {article['author']}")
        print(f"   来源: {article['source']}")
        print(f"   内容: {article['content'][:50]}...")
    else:
        print(f"\n⚠️ 没有待发布内容")
    
    # 显示所有内容列表
    data = csv_source.read_csv_data()
    print(f"\n📚 完整内容列表:")
    for i, row in enumerate(data, 1):
        status = "✅ 已发布" if row.get('已发布', '').strip().lower() in ['true', '是', '1'] else "⏳ 待发布"
        print(f"   {i}. {row.get('标题', 'Unknown')} - {status}")

if __name__ == "__main__":
    check_content_status() 